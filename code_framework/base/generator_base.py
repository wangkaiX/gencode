#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from util.python import util


class GeneratorBase:
    def __init__(self, framwork, service_dir, mako_dir, log):
        # protected
        self._framework = framwork
        self._service_dir = service_dir
        self._log = log
        self._mako_dir = mako_dir

    @property
    def adapt_name(self):
        fw = self._framework
        return "adapt_%s_%s" % (fw.service_name, fw.adapt)

    @property
    def adapt_class_name(self):
        return util.gen_upper_camel(self.adapt_name)
