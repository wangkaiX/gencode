#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from util.python import util
from code_framework.common import type_set


class GeneratorBase:
    def __init__(self, framework, service_dir, mako_dir, log):
        # protected
        self._framework = framework
        self._service_dir = service_dir
        self._log = log
        self._mako_dir = mako_dir

    @property
    def adapt_name(self):
        if self._framework.is_server:
            suffix = 'server'
        else:
            suffix = 'client'
        # return type_set.adapt_name[self._framework.adapt] + suffix
        return "%s_%s_%s" % (type_set.adapt_name[self._framework.adapt],
                             self._framework.service_name, suffix)

    @property
    def adapt_class_name(self):
        return util.gen_upper_camel(self.adapt_name)
