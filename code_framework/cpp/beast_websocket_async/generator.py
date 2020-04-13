#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from code_framework.common import tool
from util.python import util


class Generator:
    def __init__(self, mako_dir, service_dir, framework):
        self.__mako_dir = mako_dir  # os.path.join(mako_dir, 'cpp', 'websocket')
        self.__framework = framework
        self.__service_dir = service_dir
        # self.__adapt = adapt

    def gen(self):
        self.__gen_network_adapt()
        self.__gen_network()

    def __gen_network_adapt(self):
        mako_file = os.path.join(self.__mako_dir, 'adapt_server_nlohmann_json.h')
        out_file = os.path.join(self.__service_dir, 'service', 'adapt_%s_nlohmann_json.h' % self.__framework.service_name)
        tool.gen_code_file(mako_file, out_file,
                           framework=self.__framework,
                           apis=self.__framework.apis,
                           )

    def __gen_network(self):
        mako_file = os.path.join(self.__mako_dir, 'server.h')
        out_file = os.path.join(self.__service_dir, 'service', '%s.h' % self.__framework.service_name)
        tool.gen_code_file(mako_file, out_file,
                           framework=self.__framework,
                           gen_upper_camel=util.gen_upper_camel,
                           # apis=self.__framework.apis,
                           )
