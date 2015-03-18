# -*- coding: utf-8 -*-
from __future__ import absolute_import

from teerex import config

conf = config.Config()
db = conf.get("database")

try:
    imp = 'from teerex.database.%s import Database' % db
    exec imp
except:
    raise
