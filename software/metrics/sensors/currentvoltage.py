#!/usr/bin/python

import time
from lib import Subfact_ina219

class CurrentVoltage(object):
  def __init__(self, shared):
    self.shared = shared
    self.sensor = Subfact_ina219.INA219()

  def collect(self):
    data = [
      {
        'time': time.time(),
        'name': 'shunt voltage mV',
        'value': float(self.sensor.getShuntVoltage_mV())
      },
      {
        'time': time.time(),
        'name': 'bus voltage V',
        'value': float(self.sensor.getBusVoltage_V())
      },
      {
        'time': time.time(),
        'name': 'current mA',
        'value': float(self.sensor.getCurrent_mA())
      }
    ]
    time.sleep(0.1)
    return data
