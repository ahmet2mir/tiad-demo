#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""Teerex CLI.

Usage:
    teerex create <service.yaml>
    teerex delete <service.yaml>

Options:
    -h --help     Show this screen.
    --version     Show version.

"""
from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

from docopt import docopt
from teerex.teerex import Teerex

import yaml

import logging

 # Set Logger
LOGGER = logging.getLogger("teerex")
console_formatter = logging.Formatter(
            '%(filename)s:%(lineno)d\t\t\t%(message)s\n', '%m-%d %H:%M:%S')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(console_formatter)

LOGGER.addHandler(console_handler)
LOGGER.setLevel(10)
    
if __name__ == '__main__':
    arguments = docopt(__doc__, version='Teerex CLI 0.1')

    if "create" in arguments and arguments["create"]:
        f = open(arguments["<service.yaml>"])
        srv = yaml.safe_load(f)
        f.close()
        trx = Teerex(srv, "create")
        print(trx.run())

    elif "delete" in arguments and arguments["delete"]:
        f = open(arguments["<service.yaml>"])
        srv = yaml.safe_load(f)
        f.close()
        trx = Teerex(srv, "delete")
        print(trx.run())

