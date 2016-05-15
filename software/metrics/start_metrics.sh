#!/bin/bash

set -ex

python ./metrics.py --debug --mock --host http://127.0.0.1:3000/data
