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
teerex.modules.aws.instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~

AWS CRUD module for instance

 :authors: Ahmet Demir <me@ahmet2mir.eu>
"""
from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

import copy, time
import socket

try:
    import boto.ec2
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


class Instance(object):

    def __init__(self, region, aws_access_key_id, aws_secret_access_key):
        self.region = region
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.conn = boto.ec2.connect_to_region(region,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)
        self.uuid = None
        self.name = None
        self.public_dns = None


    def items(self):
        return {'uuid': self.uuid, 'name': self.name, 'public_dns': self.public_dns}


    def _find(self, name):
        reservations = self.conn.get_all_instances(filters={"tag:Name" : name})
        instances = [i for r in reservations for i in r.instances]
        if len(instances) > 0:
            self.uuid = instances[0].id
            self.name = name
            self.public_dns = instances[0].public_dns_name

            return True, "Found"

        return False, "Unable to found instance %s" % name


    def create(self, name, image_id, key_name, instance_type, security_group_ids, subnet_id, os_ready_port=22):

        f_status, _ = self._find(name)

        if f_status:
            return _response(True, self.items())
        else:
            reservation = self.conn.run_instances(image_id=image_id,\
                                             key_name=key_name,\
                                             instance_type=instance_type,\
                                             security_group_ids=[security_group_ids],\
                                             subnet_id=subnet_id)
            time.sleep(2)
            self.uuid = reservation.instances[0].id
            self.public_dns = reservation.instances[0].public_dns_name
            self.name = name
            self.conn.create_tags([self.uuid], {"Name": name})
            LOGGER.debug(self.public_dns)

            nb_times = 0
            max_nb_times = 50
            running = False
            while not running and nb_times < max_nb_times:
                reservations = self.conn.get_all_instances(instance_ids=[self.uuid])
                for reservation in reservations:
                    for instance in reservation.instances:
                        if instance.state == 'running':
                            self.uuid = instance.id
                            self.name = name
                            self.public_dns = instance.public_dns_name                            
                            LOGGER.debug("instance `{}` running!".format(instance.id))
                            running = True
                        else:
                            LOGGER.debug("instance `{}` starting...".format(instance.id))
                time.sleep(3)
                nb_times = nb_times + 1

            nb_times = 0
            os_ready = False
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            while not os_ready and nb_times < max_nb_times:
                try:
                    s.connect((self.public_dns, os_ready_port))
                    s.shutdown(2)
                    os_ready = True
                    LOGGER.debug("instance `{}` ready!".format(self.uuid))
                except:
                    pass
                    LOGGER.debug("instance `{}` progress!".format(self.uuid))

                time.sleep(3)
                nb_times = nb_times + 1

            time.sleep(3)

            if running:
                # Find and return
                s_status, s_message = self._find(name)
                if s_status:
                    return _response(True, self.items())
                else:
                    return _response(False, {}, s_message)

            return _response(False, {}, "Error occured")


    def read(self, name):
        s_status, s_message = self._find(name)
        if s_status:
            return _response(True, self.items())
        else:
            return _response(False, {}, s_message)


    # def update(self):
    #     pass


    def delete(self, name):
        s_status, s_message = self._find(name)
        if not s_status:
            return _response(True, {})
        else:
            try:
                self.conn.terminate_instances(self.uuid)
            except Exception, e:
                return _response(False, {}, str(e))

        return _response(True, {})
