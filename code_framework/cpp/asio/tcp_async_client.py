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
        mako_file = os.path.join(self.__mako_dir, 'adapt',  'nlohmann_json_client.h')
        out_file = os.path.join(self.__service_dir, self._framework.service_name, '%s.h' % self.adapt_name)
        tool.gen_code_file(mako_file, out_file,
                           framework=self.__framework,
                           apis=self.__framework.apis,
                           log=self.__log,
                           connection_class_name="TcpConnection",
                           )

    def __gen_network(self):
        mako_file = os.path.join(self.__mako_dir, 'asio', 'tcp_async_client.h')
        out_file = os.path.join(self.__service_dir, 'network', 'tcp_async_client.h')
        tool.gen_code_file(mako_file, out_file,
                           framework=self.__framework,
                           gen_upper_camel=util.gen_upper_camel,
                           log=self.__log,
                           # apis=self.__framework.apis,
                           )
