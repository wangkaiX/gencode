#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from code_framework.common import tool
from code_framework.base.generator_base import GeneratorBase
from util.python import util


class Generator(GeneratorBase):
    def __init__(self, mako_dir, dir, module, log):
        GeneratorBase.__init__(self, mako_dir=mako_dir, dir=dir, module=module, log=log)

    def gen(self):
        self.__gen_network_adapt()
        self.__gen_network()

    def __gen_network_adapt(self):
        mako_file = os.path.join(self._mako_dir, 'adapt',  'tcp_%s.h' % self._module.adapt)
        out_file = os.path.join(self._dir, self._module.name, '%s.h' % self._module.adapt_name)
        include_list = ['network/tcp_connection.h']
        tool.gen_code_file(mako_file, out_file,
                           module=self._module,
                           # apis=self._module.apis,
                           log=self._log,
                           connection_class_name="TcpConnection",
                           include_list=include_list,
                           )

    def __gen_network(self):
        mako_file = os.path.join(self._mako_dir, 'asio', 'tcp_connection.h')
        out_file = os.path.join(self._dir, 'network', 'tcp_connection.h')
        tool.gen_code_file(mako_file, out_file,
                           module=self._module,
                           gen_upper_camel=util.gen_upper_camel,
                           log=self._log,
                           # apis=self.__module.apis,
                           )
        mako_file = os.path.join(self._mako_dir, 'asio', 'tcp_connection.cpp')
        out_file = os.path.join(self._dir, 'network', 'tcp_connection.cpp')
        tool.gen_code_file(mako_file, out_file,
                           module=self._module,
                           gen_upper_camel=util.gen_upper_camel,
                           log=self._log,
                           # apis=self.__module.apis,
                           )

        if self._module.is_server:
            mako_file = os.path.join(self._mako_dir, 'asio', 'tcp_async_server.h')
            out_file = os.path.join(self._dir, self._module.name,
                                    '%s_tcp_server.h' % self._module.name)
            tool.gen_code_file(mako_file, out_file,
                               module=self._module,
                               gen_upper_camel=util.gen_upper_camel,
                               log=self._log,
                               # apis=self.__module.apis,
                               )

            mako_file = os.path.join(self._mako_dir, 'asio', 'tcp_async_server.cpp')
            out_file = os.path.join(self._dir, self._module.name,
                                    '%s_tcp_server.cpp' % self._module.name)
            tool.gen_code_file(mako_file, out_file,
                               module=self._module,
                               gen_upper_camel=util.gen_upper_camel,
                               log=self._log,
                               # apis=self.__module.apis,
                               )
