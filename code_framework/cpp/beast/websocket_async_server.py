#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from code_framework.common import tool
from code_framework.base.generator_base import GeneratorBase
from util.python import util


class Generator(GeneratorBase):
    def __init__(self, mako_dir, service_dir, framework, log):
        GeneratorBase.__init__(self, mako_dir=mako_dir, service_dir=service_dir, framework=framework, log=log)

    def gen(self):
        self.__gen_network_adapt()
        self.__gen_network()

    def __gen_network_adapt(self):
        mako_file = os.path.join(self._mako_dir, 'adapt', 'nlohmann_json_client.h')
        out_file = os.path.join(self._service_dir, 'service', '%s.h' % self.adapt_name)
        tool.gen_code_file(mako_file, out_file,
                           framework=self._framework,
                           apis=self._framework.apis,
                           log=self._log,
                           adapt_class_name=self.adapt_class_name,
                           connection_class_name="WebsocketConnection",
                           server_apis=self._framework.server_apis,
                           client_apis=self._framework.client_apis,
                           )

    def __gen_network(self):
        mako_file = os.path.join(self._mako_dir, 'beast', 'websocket_async_server.h')
        out_file = os.path.join(self._service_dir, 'network', 'websocket_async_server.h')
        tool.gen_code_file(mako_file, out_file,
                           framework=self._framework,
                           gen_upper_camel=util.gen_upper_camel,
                           log=self._log,
                           # apis=self._framework.apis,
                           )
