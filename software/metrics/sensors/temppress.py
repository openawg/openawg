import time

from random import randint
from lib import Adafruit_BMP085

class TempPress(object):
  def __init__(self, shared):
    self.shared = shared
    self.sensor = Adafruit_BMP085.BMP085()

  def collect(self):
    data = [
      {
        'time': time.time(),
        'name': 'pressure',
        'value': float(self.sensor.readPressure())
      },
      {
        'time': time.time(),
        'name': 'temperature',
        'value': float(self.sensor.readTemperature())
      },
      {
        'time': time.time(),
        'name': 'altitude',
        'value': float(self.sensor.readAltitude())
      }
    ]
    time.sleep(.1)
    return data
