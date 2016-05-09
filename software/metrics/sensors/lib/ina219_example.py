#!/usr/bin/python

import time
from Subfact_ina219 import INA219

ina = INA219()
result = ina.getBusVoltage_V()

def get_average(numbers):
	total = 0
	for number in range(numbers):
		total += ina.getBusVoltage_V()
	average = total / numbers
	return average
	

while 1:
	start_time = time.time()
	bus_voltage1 = get_average(1000)
	end_time = time.time()
	bus_voltage2 = get_average(1000)
	delta_time = end_time - start_time
	drop = bus_voltage1 - bus_voltage2
	rate = drop / delta_time
	voltage_limit = 7
	current_voltage = (bus_voltage1 + bus_voltage2) / 2
	voltage_left = current_voltage - voltage_limit
	print "Shunt   : %.3f mV" % ina.getShuntVoltage_mV()
	print "Bus     : %.3f V" % ina.getBusVoltage_V()
	print "Current : %.3f mA" % ina.getCurrent_mA()
	print "Delta time: %s" % delta_time
	print "Voltage drop: %s" % drop
	print "Voltage drop rate: %s" % rate
	print "Current voltage: %s" % current_voltage
	print "Voltage left: %s" % voltage_left
	if rate != 0:
		time_left = rate / voltage_left
	else:
		time_left = 0
	print "Time left: %s" % time_left
	time.sleep(0.1)
