#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from code_framework.common import type_set
from code_framework.common import tool
from code_framework.common.meta import Node
from code_framework.base.manager import Manager as ManagerBase
from code_framework.cpp.beast import websocket_async_server
from code_framework.cpp.asio import tcp_async_client
from util.python import util
# from data_type import err_code, err_msg, gen_title_name
# from mako.template import Template
# import util.python.util as util
# from read_config import gen_request_response


class Manager(ManagerBase):
    def __init__(self,
                 project_name,
                 # 代码格式模板目录
                 mako_dir,
                 # log
                 log,
                 # 项目生成路径
                 service_dir,
                 # 错误码配置文件
                 error_code,
                 # 错误码输出目录
                 error_outdir,
                 doc_outdir,
                 ):
        # xxx/mako/cpp
        ManagerBase.__init__(self, project_name=project_name, code_type=type_set.cpp,
                             mako_dir=mako_dir, service_dir=service_dir, error_code=error_code,
                             error_outdir=error_outdir, doc_outdir=doc_outdir, log=log)
        self._mako_dir = os.path.join(self._mako_dir, 'cpp')
        # self._service_dir = service_dir
        self._frameworks = []

    def gen(self):
        for framework in self._frameworks:
            if type_set.beast_websocket_async == framework.network:
                # mako_dir = os.path.join(self._mako_dir, 'beast_websocket_async')
                generator = websocket_async_server.Generator(mako_dir=self._mako_dir,
                                                             service_dir=self._service_dir,
                                                             framework=framework,
                                                             log=self._log,
                                                             )
                framework.adapt_name = generator.adapt_name
                framework.adapt_class_name = generator.adapt_class_name
                generator.gen()
            elif type_set.asio_tcp_async == framework.network:
                generator = tcp_async_client.Generator(mako_dir=self._mako_dir,
                                                       service_dir=self._service_dir,
                                                       framework=framework,
                                                       log=self._log,
                                                       )
                framework.adapt_name = generator.adapt_name
                framework.adapt_class_name = generator.adapt_class_name
                generator.gen()

        # types
        self._gen_types()
        self._gen_apis()
        self._gen_init()
        self._gen_main()
        self._gen_config()

    def _gen_main(self):
        mako_file = os.path.join(self._mako_dir, 'main.cpp')
        out_file = os.path.join(self._service_dir, 'main', 'main.cpp')
        tool.gen_code_file(mako_file, out_file,
                           frameworks=self._frameworks,
                           )

    def _gen_init(self):
        pass

    def _gen_config(self):
        mako_file = os.path.join(self._mako_dir, 'config.h')
        out_file = os.path.join(self._service_dir, 'config', 'config.h')
        std_includes = ['vector', 'string']
        config = {}
        for framework in self._frameworks:
            config = dict(config, **(framework.config))
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

    def _gen_types(self):
        mako_file = os.path.join(self._mako_dir, 'common', 'types.h')
        out_file = os.path.join(self._service_dir, 'common', 'types.h')
        std_includes = ['vector', 'string']
        enums = []
        nodes = []
        for framework in self._frameworks:
            nodes += framework.nodes
        nodes = tool.to_nodes(nodes)

        for framework in self._frameworks:
            enums += framework.enums

        enums = util.unique(enums)
        for enum in enums:
            print(enum)
            for value in enum.values:
                print(value)
        tool.gen_code_file(mako_file, out_file,
                           nodes=nodes,
                           std_includes=std_includes,
                           enums=enums,
                           )

    def _gen_apis(self):
        # header
        mako_file = os.path.join(self._mako_dir, 'common', 'common_api.h')
        out_file = os.path.join(self._service_dir, 'common', 'common_api.h')

        server_apis = []
        for framework in self._frameworks:
            server_apis += framework.server_apis
        server_apis = util.unique(server_apis)

        client_apis = []
        for framework in self._frameworks:
            client_apis += framework.client_apis
        client_apis = util.unique(client_apis)

        tool.gen_code_file(mako_file, out_file,
                           server_apis=server_apis,
                           client_apis=client_apis,
                           )

        mako_file = os.path.join(self._mako_dir, 'common', 'common_api.cpp')
        # apis = []
        # for framework in self._frameworks:
        #     apis += framework.apis
        for api in server_apis:
            out_file = os.path.join(self._service_dir, 'common', api.name + '.cpp')
            if not os.path.exists(out_file):
                tool.gen_code_file(mako_file, out_file,
                                   api=api,
                                   log=self._log,
                                   )
