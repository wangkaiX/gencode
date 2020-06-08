#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from code_framework.base.module_base import ModuleBase
# from code_self.common import type_set
from code_framework.common import tool
from code_framework.common import doc

import os


class TcpBase(ModuleBase):
    def __init__(self, module_name, protocol_file, error_code,
                 mako_dir, module_dir,
                 adapt,
                 heartbeat_interval_second, heartbeat_miss_max,
                 retry_count,
                 length_length,
                 no_resp,
                 ip, port,
                 is_server):
        ModuleBase.__init__(self, module_name=module_name, protocol_file=protocol_file,
                            mako_dir=mako_dir, module_dir=module_dir,
                            adapt=adapt,
                            error_code=error_code,
                            no_resp=no_resp, ip=ip, port=port, is_server=is_server)

        config = self._config[module_name]
        config["heartbeat_interval_second"] = heartbeat_interval_second
        config["heartbeat_miss_max"] = heartbeat_miss_max
        config["retry_count"] = retry_count
        config["length_length"] = length_length
        self.parser_config()

        self._cpp_mako_dir = os.path.join(mako_dir, 'cpp')
        self._length_length = length_length

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

        mako_file = os.path.join(self._cpp_mako_dir, 'module', '%s_api.h' % self.adapt)
        out_file = os.path.join(self._module_dir, self.module_name, 'api.h')
        tool.gen_code_file(mako_file, out_file,
                           module=self,
                           # include_list=include_list
                           )

        mako_file = os.path.join(self._cpp_mako_dir, 'module', '%s_api.cpp' % self.adapt)
        out_file = os.path.join(self._module_dir, self.module_name, 'api.cpp')
        tool.gen_code_file(mako_file, out_file,
                           module=self,
                           # include_list=include_list,
                           )

        # response_apis
        mako_file = os.path.join(self._cpp_mako_dir, 'module', 'response_api.cpp')
        for api in self.request_apis:
            out_file = os.path.join(self._module_dir, self.module_name, api.name + '.cpp')
            if not os.path.exists(out_file):
                tool.gen_code_file(mako_file, out_file,
                                   module=self,
                                   api=api,
                                   )
        # request_apis.h
        mako_file = os.path.join(self._cpp_mako_dir, 'module', 'request_apis.cpp')
        out_file = os.path.join(self._module_dir, self.module_name, 'request_apis.cpp')
        tool.gen_code_file(mako_file, out_file,
                           module=self,
                           )

        # types
        mako_file = os.path.join(self._cpp_mako_dir, 'module', '%s_types.h' % self.adapt)
        out_file = os.path.join(self._module_dir, self.module_name, 'types.h')
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
        out_file = os.path.join(self._module_dir, self.module_name, 'doc', '%s.md' % self.module_name)
        doc_generator = doc.Doc(mako_file=mako_file,
                                out_file=out_file,
                                apis=self.apis,
                                enums=self.enums,
                                errnos=self.error_code.errnos)
        doc_generator.gen()
