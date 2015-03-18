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
Add AWS provider

 :authors: Ahmet Demir <me@ahmet2mir.eu>
"""
from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

import datetime

try:
    from pymongo import Connection
except Exception as e:
    raise ImportError("pymongo not available. run : pip install pymongo")

DB_NAME = "database"


class AttrDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


def get_timestamp():
    return "{0}Z".format(datetime.datetime.utcnow()\
                            .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])


class Database(object):

    def __init__(self):
        self.server = Connection("172.17.42.1:27017")
        self._service = self.server[DB_NAME].service
        self._provider = self.server[DB_NAME].provider

    def add_provider(self, data):
        data['@timestamp'] = get_timestamp()
        data["_id"] = "{0}-{1}".format(data["name"], data["version"].replace(".", "_"))
        out = self._provider.insert(data)
        return out


    def get_provider(self, name, version):
        sid = "{0}-{1}".format(name, version.replace(".", "_"))
        out = list(self._provider.find({"_id":sid}))
        provider = AttrDict()
        if len(out) > 0:
            provider.name = name
            provider.version = version.replace(".", "_")
            provider.properties = out[0]
            return provider
        return {}


    def gets_provider(self):
        providers = list()
        for x in list(self._provider.find()):
            provider = AttrDict()
            fullname = x.pop('_id').split('-')
            provider.name = fullname[0]
            provider.version = fullname[1]
            provider.properties = x
            providers.append(provider)
        return providers

    def delete_provider(self, name, version):
        sid = "{0}-{1}".format(name, version.replace(".", "_"))
        return self._provider.remove({"_id":sid})


if __name__ == '__main__':

    db = Database()

    provider = {
        "name": "aws",
        "version": "v001",
        "region": "eu-west-1",
                "aws_access_key_id": 'xxxxxxxxxx',
                "aws_secret_access_key": 'xxxxxxxxxx'
      }

    print(db.add_provider(provider))

    print(db.get_provider("aws", "v001"))



