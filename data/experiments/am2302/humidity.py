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
DHT_PIN = 'P8_11'

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS = 2

DATAFILE = sys.argv[1]

print "appending to file: %s" % (DATAFILE)

while True:
    # Attempt to get sensor reading.
    humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)

    # Skip to the next reading if a valid measurement couldn't be taken.
    # This might happen if the CPU is under a lot of load and the sensor
    # can't be reliably read (timing is critical to read the sensor).
    if humidity is None or temp is None:
        print "waiting for 2 second"
        time.sleep(FREQUENCY_SECONDS)
        continue
    else:
        data = [
            {
                'time': time.time(),
                'name': 'temperature',
                'value': temp
            },
            {
                'time': time.time(),
                'name': 'humidity',
                'value': humidity
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

    time.sleep(FREQUENCY_SECONDS)
