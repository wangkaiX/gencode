#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import os
# from src.go import errno
# from src.common import tool
# from src.common import doc
# from util.python import util


class AttrBase:
    def __init__(self, **kwargs):  # protocol, mako_dir, errno_out_dir, service_dir, go_src_dir, gen_doc):
        self.__service_name = kwargs['service_name']
        self.__errno_configs = kwargs['errno_configs']
        self.__errno_out_file = kwargs['errno_out_file']
        self.__is_gen_doc = kwargs['gen_doc']
        self.__service_dir = kwargs['service_dir']
        # self.__protocol = protocol
        self.__mako_dir = kwargs['mako_dir']
        self.__kwargs = kwargs

    @property
    def kwargs(self):
        return self.__kwargs

    @property
    def service_name(self):
        return self.__service_name

    @property
    def errno_configs(self):
        return self.__errno_configs

    @property
    def errno_out_file(self):
        return self.__errno_out_file

    @property
    def is_gen_doc(self):
        return self.__is_gen_doc

    @property
    def service_dir(self):
        return self.__service_dir

    @property
    def mako_dir(self):
        return self.__mako_dir

    # @property
    # def protocol(self):
    #     return self.__protocol
