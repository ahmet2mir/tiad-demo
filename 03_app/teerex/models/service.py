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
"""
teerex.models.service
~~~~~~~~~~~~~~~~~~~~~

Teerex service

 :authors: Ahmet Demir <me@ahmet2mir.eu>
"""
from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

import base64, re
from teerex.engine import parser

from logging import getLogger
LOGGER = getLogger(__name__)

REGEX_TAG = r'(\$\{.*?\})+'
REGEX_PROPERTY = r'\$\{(.*?)\.(.*?)(\..*?)?\}'

KEYS = ["meta", "inputs", "outputs", "referentials", "providers", "resources"]

FAILED = -1
INIT = 0
PENDING = 1
FINISHED = 2

def tools(text, tag, value, action):
    v = value
    if action == ".lower":
        v = value.lower()
    elif action == ".upper":
        v = value.upper()
    elif action == ".capitalize":
        v = value.capitalize()

    return text.replace(tag, v)

def check_outputs(service):
    """
    Check if the service outputs do not contains ${}.
    :param service: service from database or user
    :returns: true if all output are setted
    """
    outputs = service["outputs"].values()
    if all(len(re.findall(REGEX_TAG, v)) == 0 for v in outputs):
        return True
    return False

def check(service):
    """
    Check if the service contains all mandatory keys.
    :param service: service from database or user
    :returns: true if is valid
    """
    if all(key in service for key in KEYS):
        return True
    return False

def set_retource_output(service, name, outputs):
    LOGGER.debug("*** Updating %s outputs with %s" % (name, outputs))
    if "resources" in service and name in service["resources"]:
        service["resources"][name]["outputs"] = outputs

def update(service, item):
    """
    Update service.
    :param item: item to update, can be resource properties, service outputs
    """
    for k, v in item.iteritems():
        if type(v) is list:
            item[k] = ",".join(v)
        elif not type(v) is str:
            item[k] = str(v)

        for tag in re.findall(REGEX_TAG, item[k]):
            for root, key, action in re.findall(REGEX_PROPERTY, tag):
                value = None
                text = item[k]
                if root == "in":
                    if key in service["inputs"]:
                        value = service["inputs"][key]
                elif root == "ref":
                    if key in service["referentials"]:
                        value = service["referentials"][key]
                else:
                    for x in service["resources"].values():
                        if "properties" in x and key in x["properties"]:
                            value = x["properties"][key]
                        elif "outputs" in x and key in x["outputs"]:
                            value = x["outputs"][key]

                if value:
                    item[k] = tools(text=text,\
                                                      tag=tag,\
                                                      value=value,\
                                                      action=action)

