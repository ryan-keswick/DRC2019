#!/bin/bash
# Starts the prgram

source race/bin/activate
pip3 install -r  requirements.txt
sleep 1
python3 ./run.py
