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
teerex.modules.docker.container
~~~~~~~~~~~~~~~~~~~~~~

Docker CRUD module for container

 :authors: Ahmet Demir <me@ahmet2mir.eu>
"""
from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

import json

try:
    from docker import Client
except:
    raise

from logging import getLogger
LOGGER = getLogger(__name__)


def _response(status, response, message=""):
    """Format proper response
    :param status: status of the action: true or False
    :param response: dict with outputs
    :param message; string message for debug
    :returns: a dict reprensting the response
    """
    return {"status": status, "response": response, "message": message}


class Container(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.base = "tcp://{0}:{1}".format(host, port)
        self.cli = Client(base_url=self.base)

        self.uuid = None


    def items(self):
        return {'uuid':self.uuid}


    def _find(self, name):
        for x in self.cli.containers(all=True):
            for n in x["Names"]:
                if "/" + name == n:
                    self.uuid = x["Id"]
                    return True, "Found"
        return False, "Unable to found container %s" % name


    def create(self, name, image, ports, volumes={}):

        f_status, _ = self._find(name)

        if f_status:
            return _response(True, self.items())
        else:
            try:
                ports_dict = {}
                for port_bind in ports.split(","):
                    port_sd = port_bind.split(":")
                    if len(port_sd) > 1:
                        ports_dict[port_sd[0]] = port_sd[1]

                # convert bindinded ports to public ports
                pub_ports = [v for v in ports_dict.values()]

                # Pull base image ?
                pull_image = True
                for i in self.cli.images():
                    for ii in i["RepoTags"]:
                        if image in ii:
                            pull_image = False

                if pull_image:
                    for line in self.cli.pull(image, stream=True):
                        LOGGER.debug(json.dumps(json.loads(line), indent=4))

                # Create the container
                container = self.cli.create_container(name=name,\
                                                      image=image,\
                                                      ports=pub_ports,\
                                                      detach=True)
                # Start it
                self.cli.start(container=container.get('Id'), port_bindings=ports_dict)
                
                # Find and return
                s_status, s_message = self._find(name)
                if s_status:
                    return _response(True, self.items())
                else:
                    return _response(False, {}, s_message)

            except Exception, e:
                LOGGER.error(e)
                return _response(False, {}, str(e))


    def read(self, name):
        s_status, s_message = self._find(name)
        if s_status:
            return _response(True, self.items())
        else:
            return _response(False, {}, s_message)


    def update(self):
        pass


    def delete(self, name, force=True):
        s_status, _ = self._find(name)
        if not s_status:
            return _response(True, {})
        else:
            try:
                self.cli.remove_container(container=self.uuid, force=force)
            except Exception, e:
                return _response(False, {}, str(e))

        return _response(True, {})
