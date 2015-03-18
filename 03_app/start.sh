#!/bin/bash

virtualenv .
source bin/activate
pip install -r requirements.txt


python teecli.py create sample01.yml