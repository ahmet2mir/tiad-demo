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
teerex.database.mongodb
~~~~~~~~~~~~~~~~~~~~~~

MongoDB database

 :authors: Ahmet Demir <me@ahmet2mir.eu>
"""
from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

import sys
from operator import itemgetter

from teerex import utils, config
from teerex.utils import AttrDict

from logging import getLogger
LOGGER = getLogger(__name__)

conf = config.Config()
conf.section = "mongodb"

try:
    from pymongo import Connection
except Exception as e:
    LOGGER.error("Unexpected error:", sys.exc_info()[0])
    LOGGER.error(e.message)
    LOGGER.exception(e)
    raise ImportError("Elasticsearch not available. run : pip install pymongo")


DB_NAME = "database"


class Database(object):

    def __init__(self):
        self.server = Connection(conf.get("host"))
        self._service = self.server[DB_NAME].service
        self._provider = self.server[DB_NAME].provider


    # PROVIDER


    def add_provider(self, data):
        data['@timestamp'] = utils.get_timestamp()
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


    # SERVICE


    def add_service(self, data):
        data['timestamp'] = utils.get_timestamp()
        data["_id"] = data["sid"]
        out = self._service.insert(data)
        return out


    def get_service(self, sid):
        out = list(self._service.find({"_id":sid}))
        if len(out) > 0:
            for name, value in out[0]['providers'].iteritems():
                if "version" in value:
                    out[0]['providers'][name] = self.get_provider(name, value["version"])
            return out[0]
        return {}


    def gets_service(self):
        services = list()
        for x in list(self._service.find()):
            service = AttrDict()
            for name, value in x['providers'].iteritems():
                if "version" in value:
                    x['providers'][name] = self.get_provider(name, value["version"])
            services.append(x)
        return services


    def delete_service(self, sid):
        return self._service.remove({"_id":sid})






