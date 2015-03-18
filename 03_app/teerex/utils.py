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
teerex.utils
~~~~~~~~~~~~~~~~~~~~~~

All util functions

 :authors: Ahmet Demir <me@ahmet2mir.eu>
"""
from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

import datetime, uuid

class AttrDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


def get_timestamp():
    return "{0}Z".format(datetime.datetime.utcnow()\
                            .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])


def normalize(string):
    """
    Normalize string
    :param string: string to normalize
    :return: the string normalized
    """
    return string.replace("_", "").replace("-", "").replace(".", "").upper()


def gen_uuid():
    """
    Generate an uuid
    :return: the uuid
    """
    return normalize(uuid.uuid1().hex).lower()
