#!/bin/bash

virtualenv .
source bin/activate
pip install -r requirements.txt

python client.py