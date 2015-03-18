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
teerex.models.provider
~~~~~~~~~~~~~~~~~~~~~~

Teerex provider model

 :authors: Ahmet Demir <me@ahmet2mir.eu>
"""
from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

def check(providers):
    if provider_name == resource["provider"] and "properties" in provider:
        resource["provider"] = provider["properties"]
    else:
        raise Exception("No properties found in provider %s" % provider_name)

