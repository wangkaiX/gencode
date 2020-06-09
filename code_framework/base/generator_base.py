#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class GeneratorBase:
    def __init__(self, module, dir, mako_dir, log):
        # protected
        self._module = module
        self._dir = dir
        self._log = log
        self._mako_dir = mako_dir
