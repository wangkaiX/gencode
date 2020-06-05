#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# from code_framework.common import generator
# from code_framework.common import meta
from code_framework.common import type_set
from code_framework import manager
from code_framework.server.tcp_server import TcpServer

if __name__ == '__main__':
    dst_dir = os.path.join("example", "cppexample_service")
    manager = manager.get_manager(
            code_type="cpp",
            project_name="project_example",
            # 代码格式模板目录
            mako_dir=os.path.join(os.environ['HOME'], 'gencode', 'mako'),
            # 项目生成路径
            service_dir=dst_dir,
            # 日志选取
            log=type_set.spdlog,
            # 接口文档输出目录:[docname].md包含所有文档，如果打了标签，则会另外生成 docname_[tag].md 命名格式的文档
            # TODO
            # 同时会生成docname.html格式的文档，与[md]格式的文档一一对应
            # doc_outdir=os.path.join(dst_dir, "doc", "docname.md"),
            )

    tcp_server_json = TcpServer(
            service_name='tcpserver_example',
            adapt=type_set.nlohmann_json,
            # 接口配置文件路径
            protocol_filename="json/api_gin.json5",
            # 错误码配置文件
            error_code_file=ec.ErrerCode("json/errno.config", 1000, 2000),
            heartbeat_interval_second=5,
            heartbeat_miss_max=3,
            length_length=8,
            no_resp=False,
            ip="127.0.0.1",
            port=12345,
            )

    manager.add(tcp_server_json)
    manager.gen()