#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from code_framework.base.server_base import ModuleBase


class TcpBase(ModuleBase):
    def __init__(self, service_name, protocol_file, error_code,
                 adapt,
                 heartbeat_interval_second, heartbeat_miss_max,
                 retry_count,
                 no_resp,
                 ip, port):
        ModuleBase.__init__(self, service_name=service_name, protocol_file=protocol_file,
                            adapt=adapt,
                            error_code=error_code, retry_count=retry_count,
                            no_resp=no_resp, ip=ip, port=port)

        config = self._config[service_name]
        config["heartbeat_interval_second"] = heartbeat_interval_second
        config["heartbeat_miss_max"] = heartbeat_miss_max
