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
teerex.config
~~~~~~~~~~~~

Teerex configuration helper. It use ConfigParser.

 :authors: Ahmet Demir <me@ahmet2mir.eu>
"""
from __future__ import absolute_import

import ConfigParser

FILE_PATH = "/etc/default/teerex.conf"

class MyParser(ConfigParser.ConfigParser):

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


class Config(object):

    def __init__(self, file=FILE_PATH):
        self.config = MyParser()
        self.config.read(file)
        self.section = "teerex"


    def get(self, name, section=None):
        search_section = self.section
        if section:
            search_section = section
        if search_section in self.config.sections() and\
             name in self.config.options(search_section):
            return self.config.get(search_section, name)
        return None

        
    def set_section(self, section):
        self.section = section


    def section_exists(self, section):
        if section in self.config.sections():
            return True
        return False

    def items(self):
        return self.config.as_dict()
