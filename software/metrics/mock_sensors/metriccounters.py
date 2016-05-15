import time
from datetime import datetime

import logging


class MetricCounters(object):

    def __init__(self, shared):
        self.logger = logging.getLogger(__name__)
        self.shared = shared

    def collect(self):
        data = []
        self.logger.debug('looping over counters')
        for key, value in self.shared.counters.iteritems():
            self.logger.debug('counter: %s' % key)
            item = {
                'time': datetime.now().isoformat(),
                'name': key,
                'value': value
            }
            data.append(item)
        time.sleep(1)
        return data
