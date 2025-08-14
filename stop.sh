#!/bin/bash
if [ -f app.pid ]; then
  kill $(cat app.pid) && rm app.pid
else
  pkill -f app.py || true
fi
