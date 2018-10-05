from selenium import webdriver
import time, json
from enum import Enum

class Platform(Enum):
    DESKTOP = 1
    MOBILE = 2

class Protocol(Enum):
    QUIC = 1
    HTTPS = 2

class Driver(object):
    executablePath = './chromedriver/chromedriver_linux'
    server_args = ["--verbose", "--log-path=./log/chromewebdriver.log"]
    desired_capabilities = {'loggingPrefs': {'performance': 'ALL'}}

    def __init__(self, platform: Platform, protocol: Protocol, domain: str):
        self.platform = platform
        self.protocol = protocol
        self.options = webdriver.ChromeOptions()
        self.webdriver = None
        self.domain = domain

    def defaultOptions(self):
        self.add_arg('--no-proxy-server')
        self.add_arg('--enable-benchmarking')
        self.add_arg('--enable-net-benchmarking')

        self.add_arg('--no-sandbox')
        self.add_arg('--incognito')

        if self.platform == Platform.MOBILE:
            self.options.add_experimental_option('androidPackage', 'com.android.chrome')

        if self.protocol == Protocol.QUIC:
            self.add_arg('--enable-quic')
            self.add_arg('--enable-quic-https')
            self.add_arg('--origin-to-force-quic-on={}:443'.format(self.domain))
            self.add_arg('--quic-host-whitelist={}'.format(self.domain))

        elif self.protocol == Protocol.HTTPS:
            self.add_arg('--disable-quic')

        return self

    def executable(self, path):
        self.executablePath = path
        return self

    def headless(self):
        self.options.set_headless()
        self.add_arg('--disable-gpu')
        self.add_arg('--no-sandbox')
        return self

    def add_arg(self, arg):
        self.options.add_argument(arg)
        return self

    def start(self):
        self.webdriver = webdriver.Chrome(
            executable_path=self.executablePath,
            desired_capabilities=self.desired_capabilities,
            chrome_options=self.options,
            service_args=self.server_args)
        return self

    def stop(self, delay = 0):
        if not delay == 0:
            time.sleep(delay)

        self.webdriver.quit()

    def delay(self, delay=5):
        time.sleep(delay)
        return self

    def clear(self):
        self.webdriver.execute_script("return chrome.benchmarking.clearCache();")
        self.webdriver.execute_script("return chrome.benchmarking.clearHostResolverCache();")
        self.webdriver.execute_script("return chrome.benchmarking.clearPredictorCache();")
        self.webdriver.execute_script("return chrome.benchmarking.closeConnections();")
        return self

    def get(self, url):
        self.webdriver.get(url)
        return self

    def dumplog(self, file='devtools.json'):
        plog = self.webdriver.execute('getLog', {'type': 'performance'})['value']
        logs = [json.loads(log['message'])['message'] for log in plog]
        with open(file, 'w') as f:
            json.dump(logs, f)

        return self

    def duration(self):
        windowPerformance = self.webdriver.execute_script(
            'var perfData = window.performance.timing; '
            'return perfData.loadEventEnd - perfData.navigationStart;'
        )

        #print log
        print(self.webdriver.execute_script(
            'String.prototype.format = function() {a = this;for (k in arguments) {a = a.replace("{" + k + "}", arguments[k])}return a};'
            'var perfData = window.performance.timing; '
            'var p1 = perfData.redirectStart - perfData.navigationStart;'
            'var p2 = perfData.redirectEnd - perfData.navigationStart;'
            'var p3 = perfData.fetchStart - perfData.navigationStart;'
            'var p4 = perfData.domainLookupStart - perfData.navigationStart;'
            'var p5 = perfData.domainLookupEnd - perfData.navigationStart;'
            'var p6 = perfData.connectStart - perfData.navigationStart;'
            'var p7 = perfData.connectEnd - perfData.navigationStart;'
            'var p8 = perfData.redirectStart - perfData.navigationStart;'
            'var p9 = perfData.responseStart - perfData.navigationStart;'
            'var p10 = perfData.responseEnd - perfData.navigationStart;'
            'var p11 = perfData.domLoading - perfData.navigationStart;'
            'var p12 = perfData.domComplete - perfData.navigationStart;'
            'var p13 = perfData.redirectStart - perfData.navigationStart;'
            'var p14 = perfData.loadEventStart - perfData.navigationStart;'
            'var total = perfData.loadEventEnd - perfData.navigationStart;'
            'var redirect = perfData.redirectEnd - perfData.redirectStart;'
            'var connection = perfData.responseEnd - perfData.requestStart;'
            'var processing = perfData.domComplete - perfData.domLoading;'
            'var load = perfData.loadEventEnd - perfData.loadEventStart;'
            'return "Request total:{0} p1:{1} p2:{2} p3:{3} p4:{4} p5:{5} p6:{6} p7:{7} p8:{8} p9:{9} p10:{10} p11:{11} p12:{12} p13:{13} p14:{14}".format(total, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14);'
        ))

        return windowPerformance
