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
    Parser
"""
from __future__ import (unicode_literals, absolute_import,
                        print_function, division) 

def parse(params):
    for k, v in params.iteritems():
        if v.startswith("${in"):
            pass
        elif v.startswith("${ref"):
            pass
        elif v.startswith("${"):
            pass      

    return params

