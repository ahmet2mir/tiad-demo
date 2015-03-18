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
teerex.engine.graph
~~~~~~~~~~~~

Teerex graph management

 :authors: Ahmet Demir <me@ahmet2mir.eu>
"""
from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

import threading
import time, random

from teerex.engine import graph
from teerex.orchestrator import Orchestrator
from teerex.models import service
from logging import getLogger
LOGGER = getLogger(__name__)

class Worker(threading.Thread):
    '''
    Based on http://effbot.org/librarybook/queue.htm
    '''
    def __init__(self, queue, svc, dgraph, name):
        self.__queue = queue
        threading.Thread.__init__(self)
        self.svc = svc
        self.name = name
        self.dgraph = dgraph

    def stop(self):
        if self.isAlive():
            threading.Thread._Thread__stop(self)

    def run(self):
        # database = Database()
        while 1:
            resource = self.__queue.get()
            if resource is None:
                # Indicate that a formerly enqueued task is complete
                self.__queue.task_done() 
                break # reached end of queue

            provider = {}

            orchestrator = Orchestrator()
            task = orchestrator.execute(resource)
            LOGGER.debug("<<<< Task result %s" % task)

            if "code" in task and task["code"]:
                # service.set_retource_output(self.svc, resource["name"], task["result"])
                if "result" in task:
                    resource["outputs"] = task["result"]
                
                self.svc["resources"][resource["name"]] = resource

                for r in self.svc["resources"].values():
                    service.update(self.svc, r["properties"])

                graph.mark_finished(self.dgraph, resource["name"])

            else:
                LOGGER.error(resource)
            
            self.__queue.task_done()


