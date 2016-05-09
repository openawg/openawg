import gevent.monkey
gevent.monkey.patch_all()

from gevent.queue import Queue

import logging
import argparse
import requests
import json
import pkgutil
import re

parser = argparse.ArgumentParser()
parser.add_argument(
    '--debug',
    help='show debug output',
    action='store_true'
)
parser.add_argument(
    '--sensor-path',
    help='path to sensor plugins',
    dest='sensor_path',
    type=str
)
parser.add_argument(
    '--mock',
    help='mock sensors, uses ./mock_sensors path',
    action='store_true'
)
parser.add_argument(
    '--log-file',
    help='path to log file',
    dest='log_file',
    type=str
)
parser.add_argument(
    '--append-log',
    help='path to append log file',
    dest='append_log',
    type=str
)
parser.add_argument(
    '--host',
    help='host and port to send metrics to',
    required=True,
    type=str
)

args = parser.parse_args()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s | %(name)s |  %(levelname)s: %(message)s'
)

stream_handler = logging.StreamHandler()

if args.debug:
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.debug('setting console logger level to DEBUG')
else:
    stream_handler.setLevel(logging.CRITICAL)
    logger.debug('setting console logger level to CRITICAL')

if args.log_file:
    log_file = args.log_file
else:
    log_file = './metrics.log'

if args.append_log:
    append_log = args.append_log
else:
    append_log = './append.log'

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.debug('setting file logger level to DEBUG')


if args.sensor_path:
    sensor_path = args.sensor_path
    pkg_name = re.sub('^\./', '', sensor_path)
else:
    sensor_path = './sensors'
    pkg_name = re.sub('^\./', '', sensor_path)

if args.mock:
    logger.debug('sensor mocking mode, using ./mock_sensors')
    sensor_path = './mock_sensors'
    pkg_name = re.sub('^\./', '', sensor_path)


class Shared():

    transmit_pool_size = 1
    metrics = Queue()

    sensors = []
    sensor_instances = []

    sensor_threads = []
    collector_threads = []

    number_sensors = 0

    threads = []

shared = Shared()

# This loads the sensor plugins in probably not a 'pythonic' way
logger.debug('looking in path: %s pkg: %s' % (sensor_path, pkg_name))
modules = pkgutil.iter_modules(path=[sensor_path])
for loader, mod_name, ispkg in modules:
    logger.debug(
        'found mod_name, ispkg: %s, %s,' %
        (mod_name, ispkg)
    )
    loaded_mod = __import__(pkg_name+'.'+mod_name, fromlist=[mod_name])
    possible_sensor_classes = []
    for item in dir(loaded_mod):
        if item.lower() == mod_name.lower():
            possible_sensor_classes.append(item)
            logger.debug('class name matches: %s' % item)

    if len(possible_sensor_classes) != 1:
        logger.debug('Cannot find sensor class in module %s' % mod_name)
        continue
    else:
        class_name = possible_sensor_classes[0]
        shared.sensors.append({
            'loaded_mod': loaded_mod,
            'class': class_name,
            'instance': getattr(loaded_mod, class_name)(shared)
        })

shared.number_sensors = len(shared.sensors)

logger.debug('Sensors found: %s' % shared.number_sensors)


def send(data):
    json_data = json.dumps(data)
    with open(append_log, 'a') as outfile:
        outfile.write(json_data + '\n')
    shared.metrics.put_nowait(json_data)


def metric_collector():
    while 1:
        metric = shared.metrics.get()

        while 1:
            try:
                headers = {
                    'Content-type': 'application/json',
                    'Accept': 'text/plain'
                }
                r = requests.post(
                    args.host,
                    headers=headers,
                    data=metric
                )
                logger.debug('Status: %s Metric: %s' % (r.status_code, metric))
                gevent.sleep()
            except:
                logger.critical('Request failed')
                continue
            break


def sensor_greenlet(sensor):
    while 1:
        data = sensor['instance'].collect()
        if isinstance(data, list):
            for item in data:
                send(item)
        else:
            send(data)
        gevent.sleep()

for number in xrange(shared.transmit_pool_size):
    logger.debug('Spawning pool worker #%s' % number)
    shared.collector_threads.append(gevent.spawn(metric_collector))

for sensor in shared.sensors:
    logger.debug('Spawning sensor greenlet: %s' % sensor['class'])
    shared.sensor_threads.append(gevent.spawn(sensor_greenlet, sensor))

shared.threads = shared.collector_threads + shared.sensor_threads

gevent.joinall(shared.threads)
