from driver import Platform, Protocol, Driver
import json

class TestObject:

    def __init__(self, url, domain):
        self.url = url
        self.domain = domain


class Test(object):

    def __init__(self, outFile, network='none'):
        self.outFile = outFile
        self.network = network
        self.results = []

    def run(self, tests):
        for test in tests:
            self.simpleDesktopHTTPSRequests(10, test.url, test.domain)
            self.simpleDesktopQUICRequests(10, test.url, test.domain)
            self.simpleMobileHTTPSRequests(10, test.url, test.domain)
            self.simpleMobileQUICRequests(10, test.url, test.domain)

        self.save()

    def simpleDesktopHTTPSRequests(self, count, url, domain):
        for x in range(count):
            driver = Driver(Platform.DESKTOP, Protocol.HTTPS, domain) \
                .defaultOptions() \
                .start() \
                .get(url)
            duration = driver.duration()
            self.results.append({'testtype': 'simple',
                                 'platform': Platform.DESKTOP.name,
                                 'protocol': Protocol.HTTPS.name,
                                 'url': url,
                                 'network': self.network,
                                 'duration': duration
                                 })

            print('{} - request {} for platform {} on protocol {} in {}ms'.format(x, url, Platform.DESKTOP.name,
                                                                          Protocol.HTTPS.name, duration))

            driver.stop(delay=0)

    def simpleMobileHTTPSRequests(self, count, url, domain):
        for x in range(count):
            driver = Driver(Platform.MOBILE, Protocol.HTTPS, domain) \
                .defaultOptions() \
                .start() \
                .get(url)
            duration = driver.duration()
            self.results.append({'testtype': 'simple',
                                 'platform': Platform.MOBILE.name,
                                 'protocol': Protocol.HTTPS.name,
                                 'url': url,
                                 'network': self.network,
                                 'duration': duration
                                 })

            print('{} - request {} for platform {} on protocol {} in {}ms'.format(x, url, Platform.MOBILE.name,
                                                                          Protocol.HTTPS.name, duration))

            driver.stop(delay=0)

    def simpleDesktopQUICRequests(self, count, url, domain):
        for x in range(count):
            driver = Driver(Platform.DESKTOP, Protocol.QUIC, domain) \
                .defaultOptions() \
                .start() \
                .get(url)
            duration = driver.duration()
            self.results.append({'testtype': 'simple',
                                 'platform': Platform.DESKTOP.name,
                                 'protocol': Protocol.QUIC.name,
                                 'url': url,
                                 'network': self.network,
                                 'duration': duration
                                 })

            print('{} - request {} for platform {} on protocol {} in {}ms'.format(x, url, Platform.DESKTOP.name,
                                                                          Protocol.QUIC.name, duration))

            driver.stop(delay=0)

    def simpleMobileQUICRequests(self, count, url, domain):
        for x in range(count):
            driver = Driver(Platform.MOBILE, Protocol.QUIC, domain) \
                .defaultOptions() \
                .start() \
                .get(url)
            duration = driver.duration()
            self.results.append({'testtype': 'simple',
                                 'platform': Platform.MOBILE.name,
                                 'protocol': Protocol.QUIC.name,
                                 'url': url,
                                 'network': self.network,
                                 'duration': duration
                                 })

            print('{} - request {} for platform {} on protocol {} in {}ms'.format(x, url, Platform.MOBILE.name,
                                                                          Protocol.QUIC.name, duration))

            driver.stop(delay=0)

    def save(self):
        with open(self.outFile, 'w') as f:
            json.dump(self.results, f)