#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from code_framework.base.module_base import ModuleBase
# from code_self.common import type_set
from code_framework.common import tool
from code_framework.common import doc

import os


class TcpBase(ModuleBase):
    def __init__(self, name, protocol_file, error_code,
                 mako_dir, dir,
                 adapt,
                 heartbeat_interval_second, heartbeat_miss_max,
                 retry_count,
                 length_length,
                 no_resp,
                 ip, port,
                 is_server):
        ModuleBase.__init__(self, name=name, protocol_file=protocol_file,
                            mako_dir=mako_dir, dir=dir,
                            adapt=adapt,
                            error_code=error_code,
                            no_resp=no_resp, ip=ip, port=port, is_server=is_server)

        config = self._config[name]
        config["heartbeat_interval_second"] = heartbeat_interval_second
        config["heartbeat_miss_max"] = heartbeat_miss_max
        config["retry_count"] = retry_count
        config["length_length"] = length_length

        self._cpp_mako_dir = os.path.join(mako_dir, 'cpp')
        self._length_length = length_length
        if is_server:
            self.__network_server_name = self._name + "_tcp_server"
            self.__network_server_class_name = self._upper_name + "TcpServer"

    @property
    def network_server_class_name(self):
        return self.__network_server_class_name

    @property
    def network_server_name(self):
        return self.__network_server_name

    @property
    def connection_class_name(self):
        return "TcpConnection"

    # def gen(self):
        # types
        # self._gen_types()
        # self._gen_apis()
        # self._gen_init()
        # self._gen_main()
        # self._gen_config()
        # self._gen_cmake()
        # self._gen_make()
        # self._gen_buildsh()

    def gen_apis(self):
        # header

        # apis.h
        # api_mako_filename_prefix = self.adapt
        if self.is_server:
            mako_file = os.path.join(self._cpp_mako_dir, 'tcp_server', 'tcp_server.h')
            out_file = os.path.join(self._dir, "%s.h" % self.__network_server_name)
            tool.gen_code_file(mako_file, out_file,
                               module=self,
                               )

            mako_file = os.path.join(self._cpp_mako_dir, 'tcp_server', 'tcp_server.cpp')
            out_file = os.path.join(self._dir, "%s.cpp" % self.__network_server_name)
            tool.gen_code_file(mako_file, out_file,
                               module=self,
                               )

        mako_file = os.path.join(self._cpp_mako_dir, 'module', '%s_api.h' % self.adapt)
        out_file = os.path.join(self._dir, 'api_impl.h')
        tool.gen_code_file(mako_file, out_file,
                           module=self,
                           # include_list=include_list
                           connection_class_name=self.connection_class_name,
                           )

        mako_file = os.path.join(self._cpp_mako_dir, 'module', '%s_api.cpp' % self.adapt)
        out_file = os.path.join(self._dir, 'api_impl.cpp')
        tool.gen_code_file(mako_file, out_file,
                           module=self,
                           )

        mako_file = os.path.join(self._cpp_mako_dir, 'module', 'api.h')
        out_file = os.path.join(self._dir, 'api.h')
        tool.gen_code_file(mako_file, out_file,
                           module=self,
                           )

        # response_apis
        mako_file = os.path.join(self._cpp_mako_dir, 'module', 'response_api.cpp')
        for api in self.response_apis:
            out_file = os.path.join(self._dir, api.name + '.cpp')
            if not os.path.exists(out_file):
                tool.gen_code_file(mako_file, out_file,
                                   module=self,
                                   api=api,
                                   )
        # request_apis.h
        mako_file = os.path.join(self._cpp_mako_dir, 'module', 'request_apis.cpp')
        out_file = os.path.join(self._dir, 'request_apis.cpp')
        tool.gen_code_file(mako_file, out_file,
                           module=self,
                           )

        # types
        mako_file = os.path.join(self._cpp_mako_dir, 'module', '%s_types.h' % self.adapt)
        out_file = os.path.join(self._dir, 'types.h')
        nodes = self.nodes
        enums = self.enums
        std_includes = ['vector', 'string']
        tool.gen_code_file(mako_file, out_file,
                           nodes=nodes,
                           std_includes=std_includes,
                           enums=enums,
                           )

        # doc
        mako_file = os.path.join(self._mako_dir, 'doc_tcp_json.md')
        out_file = os.path.join(self._dir, 'doc', '%s.md' % self.name)
        doc_generator = doc.Doc(mako_file=mako_file,
                                out_file=out_file,
                                apis=self.apis,
                                enums=self.enums,
                                errnos=self.error_code.errnos)
        doc_generator.gen()
