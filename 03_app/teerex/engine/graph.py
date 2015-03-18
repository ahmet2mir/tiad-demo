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
~~~~~~~~~~~~~~~~~~~

Teerex graph management
Read http://www.python-course.eu/graphs_python.php

May can be converted with yield and generator:
    http://sametmax.com/comment-utiliser-yield-et-les-generateurs-en-python/

 :authors: Ahmet Demir <me@ahmet2mir.eu>
"""
from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

import re

from logging import getLogger
LOGGER = getLogger(__name__)

REGEX_TAG = r'(\$\{.*?\})+'
REGEX_PROPERTY = r'\$\{(.*?)\.(.*?)(\..*?)?\}'


def build_graph(resources):
    """
    Build dependency graph with resources.
    :param resources: resources list
    :returns: a graph dependency
    """
    graph = {}
    for n, r in resources.iteritems():
        graph[n] = []
        # explicit dependency
        if "require" in r:
            for require in r["require"]:
                graph[n].append(require)
        # resource dependency
        for k, v in r["properties"].iteritems():
            for tag in re.findall(REGEX_TAG, v):
                for x in re.findall(REGEX_PROPERTY, tag):
                    graph[n].append(x[0])
    return graph


def find_runnable(graph):
    """
    Find runnable resources.
    :param graph: dependency graph
    :returns: list with runnable resource
    """
    runnable = []
    for k, v in graph.iteritems():
        if not v:
            runnable.append(k)
    return runnable


def mark_finished(graph, key):
    """
    Mark the resource as finished and remove from dependencies
    :param graph: dependency graph
    :param key: key to remove
    """
    if key in graph:
        del graph[key]
    for k, v in graph.iteritems():
        if key in v:
            graph[k].remove(key)

def to_graphviz(service):
    """
    Generate a graphviz graph.
    :param graph: dependency graph
    :returns: service in graphviz format
    """
    graph = """
        digraph unix { 
            graph [ 
                label = "Running %s version %s",
                size = "6,6"
            ];
            node [
                color=lightblue2, 
                style=filled
            ];\n""" % (service["meta"]["name"], service["meta"]["version"])
    in_graph = ""
    for name, sresource in service["resources"].iteritems():
        if "require" in sresource and sresource["require"]:
            for parent in sresource["require"]:
                in_graph = in_graph + "      " + parent + " -> " + name + ";\n"
        else:
            in_graph = in_graph + "      " + "start -> " + name + ";\n"
    graph = graph + in_graph + """
        start [shape=Mdiamond];
    }"""
    return graph