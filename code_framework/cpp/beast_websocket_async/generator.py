#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from code_framework.common import tool


class Generator:
    def __init__(self, mako_dir, service_dir, protocol):
        self.__mako_dir = mako_dir  # os.path.join(mako_dir, 'cpp', 'websocket')
        self.__protocol = protocol
        self.__service_dir = service_dir

    def gen(self):
        self.__gen_network_adapt()
        self.__gen_network()

    def __gen_network_adapt(self):
        mako_file = os.path.join(self.__mako_dir, 'adapt_nlohmann_json.h')
        out_file = os.path.join(self.__service_dir, 'service_api', 'websocket_nlohmann_json_adapt.h')
        tool.gen_code_file(mako_file, out_file,
                           protocol=self.__protocol,
                           apis=self.__protocol.apis,
                           )

    def __gen_network(self):
        mako_file = os.path.join(self.__mako_dir, 'server.h')
        out_file = os.path.join(self.__service_dir, 'network', 'websocket_server.h')
        tool.gen_code_file(mako_file, out_file,
                           # protocol=self.__protocol,
                           # apis=self.__protocol.apis,
                           )
