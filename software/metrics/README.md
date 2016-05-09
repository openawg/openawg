# Prerequisites

1. Install requirements via Pip: `pip install -r requirements.txt`

# Running the Metrics Services

Start flask server
---
`python ./server.py`

Running the metrics in mock mode
---
`./start_metrics.sh`

Start metrics script
---
`python ./metrics.py`

# Known Problems
---
1. Compiled python files `.pyc` will cause sensor plugin detection to load stale bytecode when `.py` file is not present, you can run `./cleanpyc` to remove `.pyc` files in this directory.
