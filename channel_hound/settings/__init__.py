#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

ENVIRONMENT = os.environ.setdefault("CHANNEL_ENV", "dev")

from .base import *

__mod_dir = os.path.dirname(__file__)
__mod_name = '{}.py'.format(ENVIRONMENT)
__mod_file = os.path.join(__mod_dir, __mod_name)
__namespace = locals()

if os.path.isfile(__mod_file):
    try:
        exec(open(__mod_file).read())
    except Exception as e:
        raise Exception("Failed to load settings from: '{}'.".format(__mod_file), e)
    globals().update(__namespace)
