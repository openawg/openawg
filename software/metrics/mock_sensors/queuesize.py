import time
from datetime import datetime


class QueueSize(object):
    def __init__(self, shared):
        self.shared = shared

    def collect(self):
        data = {
            'time': datetime.now().isoformat(),
            'name': 'queue.size',
            'value': self.shared.metrics.qsize()
        }
        time.sleep(1)
        return data
