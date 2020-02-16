#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.common.parser import Parser


class GeneratorBase:
    def __init__(self, framwork_type, config_files, service_name, errno_configs,
                 service_dir, mako_dir, gen_server, gen_client, gen_test,
                 gen_doc, gen_mock):
        # private
        self.__config_files = config_files
        # protected
        self._framework_type = framwork_type
        self._service_name = service_name
        self._errno_configs = errno_configs
        self._service_dir = service_dir
        self._mako_dir = mako_dir
        self._gen_server = gen_server
        self._gen_client = gen_client
        self._gen_test = gen_test
        self._gen_doc = gen_doc
        self._gen_mock = gen_mock
        # protocol
        self._protocols = []
        for config_file in config_files:
            self._protocols.append(Parser(config_file).parser())
