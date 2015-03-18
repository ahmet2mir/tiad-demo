#!/bin/bash

virtualenv .
source bin/activate
pip install -r requirements.txt

# start mongodb
fig -f mongodb.yml -p demo up -d

sleep 3

# ad provider
python add_aws.py
python add_docker.py
