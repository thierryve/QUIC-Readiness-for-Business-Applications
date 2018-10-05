from subprocess import call


class Network(object):

    def __init__(self, device="enp0s25"):
        self.device = device

    def reset(self):
        call(['sudo', 'tc', 'qdisc', 'del', 'dev', self.device, 'root', 'netem'])

    def delay(self, latency=1000):
        call(['sudo', 'tc', 'qdisc', 'add', 'dev', self.device, 'root', 'netem', 'delay', '{}ms'.format(latency)])

    def jitter(self, latency=1000, jitter=50):
        call(['sudo', 'tc', 'qdisc', 'add', 'dev', self.device, 'root', 'netem', 'delay', '{}ms'.format(latency),
              '{}ms'.format(jitter)])

    def packetloss(self, loss=0.1):
        call(['sudo', 'tc', 'qdisc', 'add', 'dev', self.device, 'root', 'netem', 'loss', '{}%'.format(loss)])

    def packetlossburst(self, loss=0.1, prob=25):
        call(['sudo', 'tc', 'qdisc', 'add', 'dev', self.device, 'root', 'netem', 'loss', '{}%'.format(loss),
              '{}%'.format(prob)])

    def duplication(self, duplicate=1):
        call(['sudo', 'tc', 'qdisc', 'add', 'dev', self.device, 'root', 'netem', 'duplicate', '{}%'.format(duplicate)])

    def corruption(self, corrupt=0.1):
        call(['sudo', 'tc', 'qdisc', 'add', 'dev', self.device, 'root', 'netem', 'corrupt', '{}%'.format(corrupt)])

    def reordering(self, delay=10, reorder=25, correlation=50):
        call(['sudo', 'tc', 'qdisc', 'add', 'dev', self.device, 'root', 'netem', 'delay', '{}ms'.format(delay),
              'reorder', '{}%'.format(reorder), '{}%'.format(correlation)])

    def international_internet_path(self):
        call(['sudo', 'tc', 'qdisc', 'add', 'dev', self.device, 'root', 'netem', 'delay', '200ms', '40ms', '25%', 'loss', '15.3%', '25%', 'duplicate', '1%', 'corrupt', '0.1%', 'reorder', '5%', '50%'])

