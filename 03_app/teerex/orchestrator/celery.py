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
teerex.orchestrator.celery
~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements Celery as orchestrator.

 :authors: Ahmet Demir <me@ahmet2mir.eu>
"""
from __future__ import (unicode_literals, absolute_import,
                        print_function, division)
import time
from teerex import config
from logging import getLogger
from teerex.database import Database

import traceback

conf = config.Config()
conf.set_section("celery")

LOGGER = getLogger(__name__)

try:
    import celery
    from kombu.common import Broadcast
    from kombu import Exchange, Queue
except Exception as e:
    raise EnvironmentError("Celery not available, install it `pip install celery`")

class Orchestrator(object):
    """
    Class to interact with Celery broker 
    """
    def __init__(self, **args):
        self.username = conf.get("username")
        self.password = conf.get("password")
        self.protocol = conf.get("protocol")
        self.host = conf.get("host")
        self.port = conf.get("port")
        self.vhost = conf.get("vhost")
        self.timeout = int(conf.get("timeout")) 

        broker_url = "{0}://{1}:{2}@{3}:{4}/{5}"\
                     .format(self.protocol,
                             self.username,
                             self.password,
                             self.host,
                             self.port,
                             self.vhost)

        self.app = celery.Celery('rex', backend='amqp', broker=broker_url)
        self.app.conf.update(
            CELERY_TASK_RESULT_EXPIRES=self.timeout,
            CELERY_TASK_SERIALIZER='json',
            CELERY_RESULT_SERIALIZER='json',
            CELERY_ACCEPT_CONTENT=['json'],
            CELERY_TIMEZONE='Europe/Paris',
            CELERY_ENABLE_UTC=True,
            CELERY_QUEUES = (
                Broadcast('broadcast_tasks'),
                Queue('run_tasks', Exchange('run_tasks'), routing_key='rex.tasks.run'),
            ),
            CELERY_ROUTES = {
                'rex.tasks.broadcast': {'queue': 'broadcast_tasks'},
                'rex.tasks.run': {'queue': 'run_tasks'}
            }
        )

    def execute(self, resource):
        """
        Exectue the resource with a Celery task
        :param resource: Resource object
        :returns: Code and return
        """
        # resource_dict["provider"] = resource.provider.items()
        try:
            provider = {}
            rex_task = self.app.send_task("rex.tasks.run", [resource])

            # database = Database()
            # task.run_id = rex_task.id
            # database.task.add(task.items())

            timeout = self.timeout - 200 # reduce to be less than celery task
            i = 0
            while not rex_task.ready() and i < timeout:
                i = i + 2
                time.sleep(2)

            if i >= timeout:
                return {"code":-1, "result": {"error": "Resource %s timeout" % resource["name"]}}

            if rex_task.successful()\
                        and rex_task.result\
                        and "status" in rex_task.result\
                        and rex_task.result["status"]:
                resource["outputs"] = rex_task.result["response"]
                return {"code":3, "result": rex_task.result["response"]}
            else:
                return {"code":-1, "result": {"error": rex_task.traceback}}
        except Exception, e:
            tb = traceback.format_exc()
            return {"code":-1, "result": {"error": str(tb)}}


            