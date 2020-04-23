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
        mako_file = os.path.join(self._mako_dir, 'adapt',  '%s.h' % self._framework.adapt)
        out_file = os.path.join(self._service_dir, self._framework.service_name, '%s.h' % self._framework.adapt_name)
        include_list = ['network/tcp_connection.h']
        tool.gen_code_file(mako_file, out_file,
                           framework=self._framework,
                           # apis=self._framework.apis,
                           log=self._log,
                           connection_class_name="TcpConnection",
                           include_list=include_list,
                           )

    def __gen_network(self):
        mako_file = os.path.join(self._mako_dir, 'asio', 'tcp_connection.h')
        out_file = os.path.join(self._service_dir, 'network', 'tcp_connection.h')
        tool.gen_code_file(mako_file, out_file,
                           framework=self._framework,
                           gen_upper_camel=util.gen_upper_camel,
                           log=self._log,
                           # apis=self.__framework.apis,
                           )

        if self._framework.is_server:
            mako_file = os.path.join(self._mako_dir, 'asio', 'tcp_async_server.h')
            out_file = os.path.join(self._service_dir, 'network', 'tcp_async_server.h')
            tool.gen_code_file(mako_file, out_file,
                               framework=self._framework,
                               gen_upper_camel=util.gen_upper_camel,
                               log=self._log,
                               # apis=self.__framework.apis,
                               )
