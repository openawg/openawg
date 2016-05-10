import time
import random
from datetime import datetime


class RandInt(object):
    def __init__(self, shared):
        self.shared = shared

    def collect(self):
        data = {
            'time': datetime.now().isoformat(),
            'name': 'mock.randint',
            'value': random.choice(range(1, 100))
        }
        time.sleep(1)
        return data
