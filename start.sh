#!/bin/bash
set -e
pip install -r requirements.txt
python app.py &
echo $! > app.pid
