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

"""Teerex exception subclasses

    Based on OpenStack Heat Exception <3
    https://github.com/openstack/heat/blob/master/heat/common/exception.py
"""

import logging, sys
import six

LOG = logging.getLogger(__name__)

_FATAL_EXCEPTION_FORMAT_ERRORS = False

class TeerexException(Exception):
    """Base Teerex Exception

    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That msg_fmt will get printf'd
    with the keyword arguments provided to the constructor.

    """
    message = "An unknown exception occurred."

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        try:
            self.message = self.msg_fmt % kwargs
        except KeyError:
            exc_info = sys.exc_info()
            # kwargs doesn't match a variable in the message
            # log the issue and the kwargs
            LOG.exception('Exception in string format operation.')
            for name, value in six.iteritems(kwargs):
                LOG.error("%s: %s" % (name, value))  # noqa

            if _FATAL_EXCEPTION_FORMAT_ERRORS:
                raise exc_info[0], exc_info[1], exc_info[2]

    def __str__(self):
        return unicode(self.message).encode('UTF-8')

    def __unicode__(self):
        return unicode(self.message)

    def __deepcopy__(self, memo):
        return self.__class__(**self.kwargs)

# Exceptions definitions here

class DummyException(TeerexException):
    """This is a Dummy exception for testing
    """
    msg_fmt = "This is a dummy exception: %(required)s."


class KeyInServiceYaml(TeerexException):
    msg_fmt = "Key %(key)s not found in the service %(service)s."


class OrchestratorNotExists(TeerexException):
    msg_fmt = "Orchestrator %(key)s not found."