#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from code_framework.base.tcp_base import TcpBase
# from code_framework.common import tool
from util.python import util
import os

concat = os.path.join


class TcpServer(TcpBase):
    def __init__(self, module_name, protocol_file, error_code,
                 mako_dir, module_dir,
                 adapt,
                 heartbeat_interval_second, heartbeat_miss_max,
                 retry_count,
                 length_length,
                 no_resp,
                 ip, port):

        TcpBase.__init__(self, module_name=module_name, protocol_file=protocol_file, error_code=error_code,
                         mako_dir=mako_dir, module_dir=module_dir,
                         adapt=adapt,
                         heartbeat_interval_second=heartbeat_interval_second, heartbeat_miss_max=heartbeat_miss_max,
                         retry_count=retry_count,
                         length_length=length_length,
                         no_resp=no_resp,
                         ip=ip, port=port,
                         is_server=True)

    def gen(self):
        self.gen_apis()
        self.gen_tcp_server()

    def gen_tcp_server(self):
        for filename in ['tcp_connection.h', 'tcp_connection.cpp', 'tcp_server.h', 'tcp_server.cpp']:
            util.copy_file(concat(self.__util_dir, filename), concat(self._module_dir, 'net', filename))
        util.copy_dir(concat(self.__util_dir, 'common'), self._module_dir, 'net', 'common')
