#!/usr/bin/python

# This script was adapted from Adafruit's Python DHT example,
# and writes each sensor reading as a JSON document
# terminated with a \n newline.

# Usage: python ./humidity.py ./datafile.txt

import sys
import time
import json

import Adafruit_DHT

# Type of sensor, can be Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT_TYPE = Adafruit_DHT.AM2302

# Example of sensor connected to Raspberry Pi pin 23
# DHT_PIN = 4
# Example of sensor connected to Beaglebone Black pin P8_11
DHT_PIN1 = 'P8_11'  # exit sensor
DHT_PIN2 = 'P8_12'  # front sensor
DHT_PIN3 = 'P8_14'  # ambient sensor

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS = 2

DATAFILE = sys.argv[1]

print "appending to file: %s" % (DATAFILE)

while True:
    humidity1 = None
    temp1 = None
    humidity2 = None
    temp2 = None
    humidity3 = None
    temp3 = None
    # Attempt to get sensor reading.
    while humidity1 is None or temp1 is None:
        print "trying sensor1..."
        humidity1, temp1 = Adafruit_DHT.read(DHT_TYPE, DHT_PIN1)
        time1 = time.time()
    print "got sensor1 data"
    while humidity2 is None or temp2 is None:
        print "trying sensor2..."
        humidity2, temp2 = Adafruit_DHT.read(DHT_TYPE, DHT_PIN2)
        time2 = time.time()
    print "got sensor2 data"
    while humidity3 is None or temp3 is None:
        print "trying sensor3..."
        humidity3, temp3 = Adafruit_DHT.read(DHT_TYPE, DHT_PIN3)
        time3 = time.time()
    print "got sensor3 data"

    # Skip to the next reading if a valid measurement couldn't be taken.
    # This might happen if the CPU is under a lot of load and the sensor
    # can't be reliably read (timing is critical to read the sensor).
    data = [
        {
            'time': time1,
            'name': 'temp1',
            'value': temp1
        },
        {
            'time': time1,
            'name': 'humidity1',
            'value': humidity1
        },
        {
            'time': time2,
            'name': 'temp2',
            'value': temp2
        },
        {
            'time': time2,
            'name': 'humidity2',
            'value': humidity2
        },
        {
            'time': time3,
            'name': 'temp3',
            'value': temp3
        },
        {
            'time': time3,
            'name': 'humidity3',
            'value': humidity3
        }
    ]
    json_data = "%s\n" % (json.dumps(data))

    try:
        print "%s" % (json_data)
        with open(DATAFILE, 'a') as f:
            f.write(json_data)
        f.close
    except:
        print "problem writing to file"
        continue
