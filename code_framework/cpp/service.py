#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
# from code_framework.common import type_set
from code_framework.common import tool
from code_framework.common.meta import Node
from code_framework.base.service_base import ServiceBase
# from code_framework.cpp.beast import websocket_async_server
# from code_framework.cpp.asio import tcp_async
# from code_framework.common import doc
# from util.python import util
# from data_type import err_code, err_msg, gen_title_name
# from mako.template import Template
# import util.python.util as util
# from read_config import gen_request_response


class CppService(ServiceBase):
    def __init__(self,
                 service_name,
                 # 代码格式模板目录
                 mako_dir,
                 # 项目生成路径
                 project_dir,
                 # 错误码
                 error_code,
                 ):
        # xxx/mako/cpp
        ServiceBase.__init__(self, service_name=service_name,
                             mako_dir=mako_dir, project_dir=project_dir,
                             error_code=error_code,
                             )
        self._cpp_mako_dir = os.path.join(self._mako_dir, 'cpp')
        # self._service_dir = service_dir

    def gen(self):
        print(self._modules)
        for module in self._modules:
            module.gen()

        # types
        # self._gen_types()
        # self._gen_apis()
        self._gen_init()
        self._gen_main()
        self._gen_config()
        self._gen_cmake()
        self._gen_make()
        self._gen_buildsh()

    def _gen_buildsh(self):
        mako_file = os.path.join(self._cpp_mako_dir, 'build.sh')
        out_file = os.path.join(self._service_dir, 'build.sh')
        tool.gen_code_file(mako_file, out_file)

    def _gen_make(self):
        mako_file = os.path.join(self._cpp_mako_dir, 'makefile')
        out_file = os.path.join(self._service_dir, 'makefile')
        tool.gen_code_file(mako_file, out_file,
                           service_name=self._service_name,
                           )

    def _gen_main(self):
        mako_file = os.path.join(self._cpp_mako_dir, 'main.cpp')
        out_file = os.path.join(self._service_dir, 'main', 'main.cpp')
        tool.gen_code_file(mako_file, out_file,
                           modules=self._modules,
                           )

    def _gen_cmake(self):
        mako_file = os.path.join(self._cpp_mako_dir, 'CMakeLists.txt')
        out_file = os.path.join(self._service_dir, 'CMakeLists.txt')
        tool.gen_code_file(mako_file, out_file,
                           service_name=self._service_name,
                           modules=self._modules,
                           )

    def _gen_init(self):
        pass

    def _gen_config(self):
        mako_file = os.path.join(self._cpp_mako_dir, 'config.h')
        out_file = os.path.join(self._service_dir, 'config', 'config.h')
        std_includes = ['vector', 'string']
        config = {}
        for module in self._modules:
            config = dict(config, **(module.config))
        print("config:", config)
        node = Node(None, "config", config)
        nodes = tool.to_nodes(node)

        tool.gen_code_file(mako_file, out_file,
                           nodes=nodes,
                           std_includes=std_includes,
                           )
        out_file = os.path.join(self._service_dir, "config.json")
        with open(out_file, "w") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
