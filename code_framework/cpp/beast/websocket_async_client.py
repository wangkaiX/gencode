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
        mako_file = os.path.join(self._mako_dir, 'adapt', 'nlohmann_json.h')
        out_file = os.path.join(self._dir, self._module.name, '%s.h' % self.adapt_name)
        include_list = ['network/websocket_connection.h']
        tool.gen_code_file(mako_file, out_file,
                           module=self._module,
                           apis=self._module.apis,
                           log=self._log,
                           adapt_class_name=self.adapt_class_name,
                           connection_class_name="WebsocketConnection",
                           request_apis=self._module.request_apis,
                           request_apis=self._module.request_apis,
                           include_list=include_list,
                           )

    def __gen_network(self):
        mako_file = os.path.join(self._mako_dir, 'beast', 'websocket_connection.h')
        out_file = os.path.join(self._dir, 'network', 'websocket_connection.h')
        tool.gen_code_file(mako_file, out_file,
                           module=self._module,
                           gen_upper_camel=util.gen_upper_camel,
                           log=self._log,
                           # apis=self._module.apis,
                           )
