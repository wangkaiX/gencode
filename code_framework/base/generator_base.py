#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class GeneratorBase:
    def __init__(self, framework, service_dir, mako_dir, log):
        # protected
        self._framework = framework
        self._service_dir = service_dir
        self._log = log
        self._mako_dir = mako_dir
