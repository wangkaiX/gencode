#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# from code_framework.common import generator
# from code_framework.common import meta
from code_framework.common import type_set
from code_framework.common import error_code as ec
from code_framework.cpp.service import CppService
from code_framework.server.tcp_server import TcpServer

if __name__ == '__main__':
    dst_dir = os.path.join("example", "cppexample_service")
    mako_dir = os.path.join(os.environ['HOME'], 'gencode', 'mako')
    # manager = manager.get_manager(
    #         code_type="cpp",
    #         service_name="project_example",
    #         # 代码格式模板目录
    #         mako_dir=mako_dir,
    #         # 项目生成路径
    #         service_dir=dst_dir,
    #         # 日志选取
    #         log=type_set.spdlog,
    #         # 接口文档输出目录:[docname].md包含所有文档，如果打了标签，则会另外生成 docname_[tag].md 命名格式的文档
    #         # TODO
    #         # 同时会生成docname.html格式的文档，与[md]格式的文档一一对应
    #         # doc_outdir=os.path.join(dst_dir, "doc", "docname.md"),
    #         )

    tcp_server_json = TcpServer(
            name='tcpserver_example',
            adapt=type_set.nlohmann_json,
            mako_dir=mako_dir,
            dir=os.path.join(dst_dir, 'tcpserver_example'),
            # 接口配置文件路径
            protocol_file="json/api_gin.json5",
            # 错误码配置文件
            error_code=ec.ErrerCode("json/errno.config", 1000, 2000),
            heartbeat_interval_second=5,
            heartbeat_miss_max=3,
            retry_count=3,
            length_length=8,
            no_resp=False,
            ip="127.0.0.1",
            port=12345,
            )

    # tcp_server_json.gen()
    cpp_example_service = CppService(
            service_name="cpp_example_service",
            mako_dir=mako_dir,
            service_dir=dst_dir,
            error_code=ec.ErrerCode("json/errno.config", 1000, 2000),
            )
    cpp_example_service.add(tcp_server_json)
    cpp_example_service.gen()
