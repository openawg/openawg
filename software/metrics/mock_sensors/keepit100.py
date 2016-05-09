import time


class KeepIt100(object):
    def __init__(self, shared):
        self.shared = shared

    def collect(self):
        data = {
            'time': time.time(),
            'name': 'mock.metric',
            'value': 100
        }
        time.sleep(1)
        return data
