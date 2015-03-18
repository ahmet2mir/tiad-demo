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
teerex.models.resource
~~~~~~~~~~~~~~~~~~~~~~

Teerex resource model

 :authors: Ahmet Demir <me@ahmet2mir.eu>
"""
from __future__ import (unicode_literals, absolute_import,
                        print_function, division)


import re
from logging import getLogger
LOGGER = getLogger(__name__)

FAILED = -1
INIT = 0
PENDING = 1
FORKED = 2
FINISHED = 3

REGEX_TAG = r'(\$\{.*?\})+'

KEYS = ["name", "version", "type", "id", "properties"]
KEYS_OPTIONAL = ["require", "lifecycle", "returns", "outputs"]

from teerex.database import Database


def build(resource, name, sid, providers, action):
    """
    Build the resource with name version and id from service.
    :param resource: resource from database or user
    :param name: resource name in the service
    :param sid: unique id
    :param providers: providers list
    :param sid: resource action: CRUD or an action
    """
    if not "name" in resource:  
        resource["name"] = name
    if not "id" in resource:
        resource["id"] = sid
    if not "lifecycle" in resource:
        resource["lifecycle"] = action
    elif not resource["lifecycle"]:
        resource["lifecycle"] = action

    for provider_name, provider in providers.iteritems():

        if resource["provider"] == provider_name:
            if "version" in provider:
                resource["version"] = provider["version"]
                db = Database()
                db_provider = db.get_provider(provider_name, provider["version"])
                if db_provider:
                    resource["provider"] = db_provider
                else:
                    raise Exception("No provider %s" % provider_name)
            else:
                raise Exception("No version found in provider %s" % provider_name)

    
    # initialize unsetted optional fields
    for r in KEYS_OPTIONAL:
        if not r in resource.keys():
            resource[r] = None


def is_valid(resource):
    """
    Check if the resource contains all mandatory keys.
    :param resource: resource from database or user
    :returns: true if is valid
    """
    if all(key in resource.keys() for key in KEYS):
        return True
    return False


def is_runnable(resource):
    """
    Check if all properties of the resource
    doesn't have variable i.e ${xxx}.
    :param resource: resource to check
    :returns: true is the resource is runnable
    """
    runnable = True
    for x in resource["properties"].values():
        if not len(re.findall(REGEX_TAG, x)) == 0:
            runnable = False
    return runnable
