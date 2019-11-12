#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from mako.template import Template
import os
# from src.common import meta
from src.common import errno
from src.common import tool

# from gencode.common import tool
# import util.python.util as util


class GoErrnoGen(errno.ErrnoGen):
    def __init__(self, mako_file, out_file, errno_configs):  # config_file, begin_no, end_no):
        errno.ErrnoGen.__init__(errno_configs)
        self.__mako_file = mako_file
        self.__out_file = out_file
        self.__package_name = os.path.basename(os.path.dirname(out_file))

    def gen_code(self):
        self.parser()
        text = tool.gen_code_file(self.__mako_file, self.__out_file, errnos=self.__errnos, package_name=self.__package_name)
        return text
