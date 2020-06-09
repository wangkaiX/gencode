#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import os
# from src.go import errno
from src.base.protocol_generator_base import ProtocolGeneratorBase
from src.common import tool
# from src.common import doc
# from util.python import util


class GoProtocolGeneratorBase(ProtocolGeneratorBase):
    def __init__(self, protocol, **kwargs):  # protocol, mako_dir, errno_out_dir, dir, go_src_dir, gen_doc):
        ProtocolGeneratorBase.__init__(self, protocol, **kwargs)
        self.__go_src_dir = kwargs['go_src_dir']
        self.__package_dir = tool.package_name(self.dir, self.__go_src_dir)
        self.__package_errno_dir = tool.package_name(self.errno_dir, self.go_src_dir)
        # self.__name = kwargs['name']

    @property
    def package_errno_dir(self):
        return self.__package_errno_dir

    @property
    def package_dir(self):
        return self.__package_dir

    @property
    def go_src_dir(self):
        return self.__go_src_dir

    def gen_code(self):
        ProtocolGeneratorBase.gen_code(self)
        # self.gen_errno()
        self.gen_init()
        self.gen_api()
        self.gen_test()

    def init_test(self, test_dir):
        pass
        # mako_file = os.path.join(self.mako_dir, 'go', 'test_init.go')
        # filename = os.path.join(test_dir, 'test_init.go')
        # tool.gen_code_file(mako_file, filename, package_dir=self.__package_dir)

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
        out_file = os.path.join(self.__dir, 'app', 'define', 'config.go')
        tool.gen_code_file(mako_file, out_file, configs=configs, gen_upper_camel=util.gen_upper_camel)
        # config.toml
        mako_file = os.path.join(self.mako_dir, 'go', 'config.toml')
        out_file = os.path.join(self.dir, 'configs', 'config.toml')
        tool.gen_code_file(mako_file, out_file, configs=configs)

    def gen_init(self):
        out_file = os.path.join(self.__dir, 'cmd', 'init.go')
        if not os.path.exists(out_file):
            mako_file = os.path.join(self.__mako_dir, 'go', 'init.go')
            tool.gen_code_file(mako_file, out_file)
    '''
