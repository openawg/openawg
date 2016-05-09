
import gevent.monkey
gevent.monkey.patch_all()

from gevent.queue import Queue
from gevent.pool import Pool

import time
import requests
import json
import pkgutil
import inspect

from random import randint

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

modules = pkgutil.iter_modules(path=["./sensors"])
for loader, mod_name, ispkg in modules: 
  loaded_mod = __import__("sensors."+mod_name, fromlist=[mod_name])
  possible_sensor_classes = []
  for item in dir(loaded_mod):
    if item.lower() == mod_name.lower():
      possible_sensor_classes.append(item)

  if len(possible_sensor_classes) != 1:
    print "Cannot find sensor class in module %s" % mod_name
    continue
  else:
    class_name = possible_sensor_classes[0]
    shared.sensors.append({
      'loaded_mod': loaded_mod,
      'class': class_name,
      'instance': getattr(loaded_mod, class_name)(shared)
    })

shared.number_sensors = len(shared.sensors)

print "Sensors found: %s" % shared.number_sensors


def send(data):
  with open("./logfile", "a") as outfile:
    outfile.write(json.dumps(data) + "\n")
  shared.metrics.put_nowait(data)

def metric_collector():
  while 1:
    metric = shared.metrics.get()

    while 1:
      try:
        #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        #r = requests.post("http://192.168.2.5:5000", data=metric)
        #print "Status: %s Metric: %s" % (r.status_code, metric)
        print "Value: %s Metric: %s" % (metric['value'], metric['name'])
        gevent.sleep()
      except:
        print "Request failed, retrying."
        continue
      break

def sensor_greenlet(sensor):
  while 1:
    data = sensor['instance'].collect()
    if isinstance(data, list):
      for item in data:
        send(item)
    else: send(data)
    gevent.sleep()

for number in xrange(shared.transmit_pool_size):
  print "Spawning pool worker #%s" % number 
  shared.collector_threads.append(gevent.spawn(metric_collector))

for sensor in shared.sensors:
  print "Spawning sensor greenlet: %s" % sensor['class']
  shared.sensor_threads.append(gevent.spawn(sensor_greenlet, sensor))

shared.threads = shared.collector_threads + shared.sensor_threads

gevent.joinall(shared.threads)

