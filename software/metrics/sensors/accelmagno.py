import time

from random import randint
from lib import Adafruit_LSM303

class AccelMagno(object):
  def __init__(self, shared):
    self.shared = shared
    self.sensor = Adafruit_LSM303.Adafruit_LSM303()

  def collect(self):
    sensor_data = self.sensor.read()
    data = [
      {
        'time': time.time(),
        'name': 'accelerometer x',
        'value': float(sensor_data[0][0])
      },
      {
        'time': time.time(),
        'name': 'accelerometer y',
        'value': float(sensor_data[0][1])
      },
      {
        'time': time.time(),
        'name': 'accelerometer z',
        'value': float(sensor_data[0][2])
      },
      {
        'time': time.time(),
        'name': 'magnometer x',
        'value': float(sensor_data[1][0])
      },
      {
        'time': time.time(),
        'name': 'magnometer y',
        'value': float(sensor_data[1][1])
      },
      {
        'time': time.time(),
        'name': 'magnometer z',
        'value': float(sensor_data[1][2])
      },
      {
        'time': time.time(),
        'name': 'magnometer orientation',
        'value': float(sensor_data[1][3])
      }
    ]
    time.sleep(0.1)
    return data
