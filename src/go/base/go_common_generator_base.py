#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import os
# from src.go import errno
from src.base.common_generator_base import CommonGeneratorBase
from src.common import tool
# from src.common import doc
# from util.python import util


class GoCommonGeneratorBase(CommonGeneratorBase):
    def __init__(self, protocol, **kwargs):  # protocol, mako_dir, errno_out_dir, service_dir, go_src_dir, gen_doc):
        CommonGeneratorBase.__init__(self, protocol, **kwargs)
        self.__go_src_dir = kwargs['go_src_dir']
        self.__package_service = tool.package_name(self.service_dir, self.__go_src_dir)
        # self.__service_name = kwargs['service_name']

    @property
    def package_service(self):
        return self.__package_service

    @property
    def go_src_dir(self):
        return self.__go_src_dir

    def gen_code(self):
        CommonGeneratorBase.gen_code(self)
        # self.gen_errno()
        self.gen_init()

    # def gen_errno(self):
    #     errno_mako = os.path.join(self.mako_dir, 'go', 'errno.go')
    #     errno_gen = errno.GoErrnoGen(errno_mako, self.errno_out_file, self.errno_configs)
    #     errno_gen.gen_code()

    '''
    def gen_config(self, configs=None):
        if not configs:
            configs = self.__protocol.configs
        self.__gen_config(configs)

    def __gen_config(self, configs):
        # config.go
        mako_file = os.path.join(self.__mako_dir, 'go', 'config.go')
        out_file = os.path.join(self.__service_dir, 'app', 'define', 'config.go')
        tool.gen_code_file(mako_file, out_file, configs=configs, gen_upper_camel=util.gen_upper_camel)
        # config.toml
        mako_file = os.path.join(self.mako_dir, 'go', 'config.toml')
        out_file = os.path.join(self.service_dir, 'configs', 'config.toml')
        tool.gen_code_file(mako_file, out_file, configs=configs)

    def gen_init(self):
        out_file = os.path.join(self.__service_dir, 'cmd', 'init.go')
        if not os.path.exists(out_file):
            mako_file = os.path.join(self.__mako_dir, 'go', 'init.go')
            tool.gen_code_file(mako_file, out_file)
    '''
