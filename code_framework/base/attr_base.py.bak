#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.common import errno


class AttrBase:
    def __init__(self, service_name, errno_configs, mako_dir, errno_dir, service_dir, go_src_dir, gen_doc):
        self.__service_name = service_name
        self.__errno_dir = errno_dir
        self.__gen_doc = gen_doc
        self.__service_dir = service_dir
        self.__mako_dir = mako_dir

        errno_gen = errno.ErrnoGen(errno_configs)
        self.__errnos = errno_gen.errnos

    @property
    def errnos(self):
        return self.__errnos

    @property
    def service_name(self):
        return self.__service_name

    # @property
    # def errno_configs(self):
    #     return self.__errno_configs

    @property
    def errno_dir(self):
        return self.__errno_dir

    @property
    def gen_doc(self):
        return self.__gen_doc

    @property
    def service_dir(self):
        return self.__service_dir

    @property
    def mako_dir(self):
        return self.__mako_dir

    # @property
    # def protocol(self):
    #     return self.__protocol
