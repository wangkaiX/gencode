#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class GeneratorBase:
    def __init__(self, module, module_dir, mako_dir, log):
        # protected
        self._module = module
        self._module_dir = module_dir
        self._log = log
        self._mako_dir = mako_dir
