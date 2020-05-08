#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from code_framework.common import type_set
from code_framework.common import tool
from code_framework.common.meta import Node
from code_framework.base.manager import Manager as ManagerBase
from code_framework.cpp.beast import websocket_async_server
from code_framework.cpp.asio import tcp_async
from code_framework.common import doc
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
                 # error_code,
                 # 错误码输出目录
                 # error_outdir,
                 # doc_outdir,
                 ):
        # xxx/mako/cpp
        ManagerBase.__init__(self, project_name=project_name, code_type=type_set.cpp,
                             mako_dir=mako_dir, service_dir=service_dir,
                             # error_code=error_code,
                             # error_outdir=error_outdir,
                             # doc_outdir=doc_outdir,
                             log=log)
        self._cpp_mako_dir = os.path.join(self._mako_dir, 'cpp')
        # self._service_dir = service_dir
        self._frameworks = []

    def gen(self):
        for framework in self._frameworks:
            if type_set.beast_websocket_async == framework.network:
                # mako_dir = os.path.join(self._cpp_mako_dir, 'beast_websocket_async')
                generator = websocket_async_server.Generator(mako_dir=self._cpp_mako_dir,
                                                             service_dir=self._service_dir,
                                                             framework=framework,
                                                             log=self._log,
                                                             )
            elif type_set.asio_tcp_async == framework.network:
                generator = tcp_async.Generator(mako_dir=self._cpp_mako_dir,
                                                service_dir=self._service_dir,
                                                framework=framework,
                                                log=self._log,
                                                )
            generator.gen()

        # types
        # self._gen_types()
        self._gen_apis()
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
                           project_name=self._project_name,
                           )

    def _gen_main(self):
        mako_file = os.path.join(self._cpp_mako_dir, 'main.cpp')
        out_file = os.path.join(self._service_dir, 'main', 'main.cpp')
        tool.gen_code_file(mako_file, out_file,
                           frameworks=self._frameworks,
                           )

    def _gen_cmake(self):
        mako_file = os.path.join(self._cpp_mako_dir, 'CMakeLists.txt')
        out_file = os.path.join(self._service_dir, 'CMakeLists.txt')
        tool.gen_code_file(mako_file, out_file,
                           project_name=self._project_name,
                           frameworks=self._frameworks,
                           )

    def _gen_init(self):
        pass

    def _gen_config(self):
        mako_file = os.path.join(self._cpp_mako_dir, 'config.h')
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
        mako_file = os.path.join(self._cpp_mako_dir, 'common', 'types.h')
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

        for framework in self._frameworks:
            server_apis = framework.server_apis
            server_apis = util.unique(server_apis)
            client_apis = framework.client_apis
            client_apis = util.unique(client_apis)

            if type_set.beast_websocket_async == framework.network:
                include_list = ["network/websocket_connection.h"]
                connection_class_name = "WebsocketConnection"
            elif type_set.asio_tcp_async == framework.network:
                include_list = ["network/tcp_connection.h"]
                connection_class_name = "TcpConnection"
            else:
                assert False

            # apis.h
            if framework.adapt == type_set.nlohmann_json:
                api_mako_filename_prefix = 'nlohmann_json'
            elif framework.adapt == type_set.binary:
                api_mako_filename_prefix = 'binary'
            else:
                assert False
            mako_file = os.path.join(self._cpp_mako_dir, 'service', '%s_api.h' % api_mako_filename_prefix)
            out_file = os.path.join(self._service_dir, framework.service_name, 'api.h')
            tool.gen_code_file(mako_file, out_file,
                               framework=framework,
                               adapt_name=framework.adapt_name,
                               adapt_class_name=framework.adapt_class_name,
                               include_list=include_list,
                               connection_class_name=connection_class_name,
                               )

            mako_file = os.path.join(self._cpp_mako_dir, 'service', '%s_api.cpp' % api_mako_filename_prefix)
            out_file = os.path.join(self._service_dir, framework.service_name, 'api.cpp')
            tool.gen_code_file(mako_file, out_file,
                               framework=framework,
                               adapt_name=framework.adapt_name,
                               adapt_class_name=framework.adapt_class_name,
                               include_list=include_list,
                               connection_class_name=connection_class_name,
                               )

            # server_apis
            mako_file = os.path.join(self._cpp_mako_dir, 'service', 'server_api.cpp')
            for api in server_apis:
                out_file = os.path.join(self._service_dir, framework.service_name, api.name + '.cpp')
                if not os.path.exists(out_file):
                    tool.gen_code_file(mako_file, out_file,
                                       framework=framework,
                                       # no_resp=framework.no_resp,
                                       api=api,
                                       log=self._log,
                                       )
            # client_apis.h
            mako_file = os.path.join(self._cpp_mako_dir, 'service', 'client_apis.cpp')
            out_file = os.path.join(self._service_dir, framework.service_name, 'client_apis.cpp')
            tool.gen_code_file(mako_file, out_file,
                               framework=framework,
                               # no_resp=framework.no_resp,
                               # server_apis=server_apis,
                               # client_apis=client_apis,
                               )

            # types
            mako_file = os.path.join(self._cpp_mako_dir, 'service', '%s_types.h' % api_mako_filename_prefix)
            out_file = os.path.join(self._service_dir, framework.service_name, 'types.h')
            nodes = framework.nodes
            enums = framework.enums
            std_includes = ['vector', 'string']
            tool.gen_code_file(mako_file, out_file,
                               nodes=nodes,
                               std_includes=std_includes,
                               enums=enums,
                               )

            # doc
            mako_file = os.path.join(self._mako_dir, 'doc_tcp_json.md')
            out_file = os.path.join(self._service_dir, framework.service_name, 'doc', '%s.md' % framework.service_name)
            doc_generator = doc.Doc(mako_file=mako_file,
                                    out_file=out_file,
                                    apis=framework.apis,
                                    enums=framework.enums,
                                    errnos=framework.error_code.errnos)
            doc_generator.gen()
