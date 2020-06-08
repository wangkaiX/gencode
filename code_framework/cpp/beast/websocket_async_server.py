#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from code_framework.common import tool
from code_framework.base.generator_base import GeneratorBase
from util.python import util


class Generator(GeneratorBase):
    def __init__(self, mako_dir, module_dir, module, log):
        GeneratorBase.__init__(self, mako_dir=mako_dir, module_dir=module_dir, module=module, log=log)

    def gen(self):
        self.__gen_network_adapt()
        self.__gen_network()

    def __gen_network_adapt(self):
        mako_file = os.path.join(self._mako_dir, 'adapt', '%s.h' % self._module.adapt)
        out_file = os.path.join(self._module_dir, self._module.module_name, '%s.h' % self._module.adapt_name)
        include_list = ['network/websocket_connection.h']
        tool.gen_code_file(mako_file, out_file,
                           module=self._module,
                           apis=self._module.apis,
                           log=self._log,
                           connection_class_name="WebsocketConnection",
                           request_apis=self._module.request_apis,
                           request_apis=self._module.request_apis,
                           include_list=include_list,
                           )

    def __gen_network(self):
        mako_file = os.path.join(self._mako_dir, 'beast', 'websocket_async_server.h')
        out_file = os.path.join(self._module_dir, 'network', 'websocket_async_server.h')
        tool.gen_code_file(mako_file, out_file,
                           module=self._module,
                           gen_upper_camel=util.gen_upper_camel,
                           log=self._log,
                           # apis=self._module.apis,
                           )

        mako_file = os.path.join(self._mako_dir, 'beast', 'websocket_connection.h')
        out_file = os.path.join(self._module_dir, 'network', 'websocket_connection.h')
        tool.gen_code_file(mako_file, out_file,
                           module=self._module,
                           gen_upper_camel=util.gen_upper_camel,
                           log=self._log,
                           # apis=self._module.apis,
                           )
