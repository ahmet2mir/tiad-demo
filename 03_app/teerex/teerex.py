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
teerex.teerex
~~~~~~~~~~~~~~~~~~~~~~

Teerex main package

 :authors: Ahmet Demir <me@ahmet2mir.eu>
"""
from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

from teerex.exception import KeyInServiceYaml
from teerex.engine import graph
from teerex.engine.worker import Worker
from teerex.models import service, resource

from teerex import utils

from Queue import Queue

import sys, re
import yaml, json, time

from logging import getLogger
LOGGER = getLogger(__name__)

class Teerex(object):

    def __init__(self, srv, action, run_id=None):
        self.srv = utils.AttrDict(srv)
        self.action = action
        self.run_id = run_id
        if not run_id:
            self.run_id = utils.gen_uuid()


    def run(self):

        num_workers = 2
        queue = Queue(0)
        workers = list()

        try:
            if not service.check(self.srv):
                raise KeyInServiceYaml(key=",".join([key for key in self.srv.keys()]), service=self.srv)
            else:
                LOGGER.debug(">>>> Service check %s" % service.check(self.srv))

            providers = self.srv.providers

            # update services and resources
            for r in self.srv.resources.values():
                service.update(self.srv, r["properties"])

            self.srv.name = self.srv.meta["name"]
            self.srv.version = self.srv.meta["version"]
            self.srv.id = self.run_id
            self.srv.action = self.action

            # LOGGER.debug(graph.to_graphviz(self.srv))
            LOGGER.debug(">>>> Updated resources %s" % self.srv.resources)

            # build dependency grapsvch
            dgraph = graph.build_graph(self.srv.resources)
            LOGGER.debug(">>>> Dependency Graph %s" % dgraph)

            # init workers
            for i in range(num_workers):
                worker = Worker(queue, self.srv, dgraph, "worker--{0}".format(i))
                worker.start() # start a worker
                workers.append(worker)

            timeout = 500
            t_start = time.time()
            t_pending = 0

            LOGGER.debug(">>>> Service %s" % self.srv)
            # each time a resource is finished, remove it from graph
            # then loop while it's not empty or timed out
            while dgraph and t_pending < timeout:
                for r_name in graph.find_runnable(dgraph):
                    rsc = utils.AttrDict(self.srv.resources[r_name])

                    # build the resource and set "unsetted" params
                    resource.build(rsc, r_name, self.srv.id, providers, self.srv.action)
                    
                    if resource.is_runnable(rsc):
                        LOGGER.debug(">>>> Run %s: %s" % (r_name, rsc))
                        # remove resource from graph 
                        # but keep dependency in other resources
                        del dgraph[r_name]
                        queue.put(rsc)
                        # graph.mark_finished(dgraph, r_name)

                # elasped time
                t_pending = time.time() - t_start
                time.sleep(0.3)

            # add end-of-self.queue "markers"
            for i in range(num_workers):
                queue.put(None) 
         
            # blocks until all items in the queue 
            # have been gotten and processed.
            queue.join()

            for worker in workers:
                worker.stop()

            # if the dependency graph is not empty, something wrong occurs
            # or the execution timed out
            if dgraph:
                LOGGER.debug("<<<< Timeout")
                LOGGER.debug("<<<< Not executed %s" % dgraph)
                return False, {}
            else:
                LOGGER.debug("<<<< Finished")

            # update desired outputs from user
            if "outputs" in self.srv:
                service.update(self.srv, self.srv.outputs)

            # if an output contains ${}, exec error
            if service.check_outputs(self.srv):
                return True, json.dumps(self.srv.outputs)

            return False, {}

        except KeyInServiceYaml as e:
            LOGGER.error(e.message)
            return False, {}

        except Exception as e:
            LOGGER.error("<<<< Unexpected error: %s" % sys.exc_info()[0])
            LOGGER.error("<<<< %s" % e.message)
            LOGGER.exception(e)
            return False, {}


