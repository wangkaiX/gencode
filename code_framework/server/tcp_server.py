#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from code_framework.base.tcp_base import TcpBase
from util.python import util


class TcpServer(TcpBase):
    def __init__(self, service_name, protocol_file, error_code,
                 adapt,
                 heartbeat_interval_second, heartbeat_miss_max,
                 retry_count,
                 no_resp,
                 ip, port):

        TcpBase.__init__(self, service_name=service_name, protocol_file=protocol_file, error_code=error_code,
                         adapt=adapt,
                         heartbeat_interval_second=heartbeat_interval_second, heartbeat_miss_max=heartbeat_miss_max,
                         retry_count=retry_count,
                         no_resp=no_resp,
                         ip=ip, port=port)

        self.__service_class_name = util.gen_upper_camel("%s_%s" % (service_name, 'server'))
