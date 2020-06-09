#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from code_framework.base.tcp_base import TcpBase
# from code_framework.common import tool
from util.python import util
import os

concat = os.path.join


class TcpClient(TcpBase):
    def __init__(self, name, protocol_file, error_code,
                 project_dir,
                 mako_dir,
                 adapt,
                 heartbeat_interval_second, heartbeat_miss_max,
                 retry_count,
                 length_length,
                 no_resp,
                 ip, port):

        TcpBase.__init__(self, name=name, protocol_file=protocol_file, error_code=error_code,
                         mako_dir=mako_dir, project_dir=project_dir,
                         adapt=adapt,
                         heartbeat_interval_second=heartbeat_interval_second, heartbeat_miss_max=heartbeat_miss_max,
                         retry_count=retry_count,
                         length_length=length_length,
                         no_resp=no_resp,
                         ip=ip, port=port,
                         is_server=False)

    def gen(self):
        self.gen_apis()
        self.gen_tcp_client()

    def gen_tcp_client(self):
        tcp_dir = concat(self._util_dir, 'cpp', 'tcp')
        for filename in ['tcp_connection.h', 'tcp_connection.cpp']:
            util.copy_file(concat(tcp_dir, filename), concat(self._project_dir, 'common', 'net', filename))
        util.copy_dir(concat(self._util_dir, 'cpp', 'common'), concat(self._project_dir, 'common', 'net', 'common'))
