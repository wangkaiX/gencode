#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# from mako.template import Template
import util.python.util as util
from src.common import tool
from src.go.generator import GoGenerator
# import copy


class GoGinGenerator(GoGenerator):
    def __init__(self, **kwargs):
        GoGenerator.__init__(self, **kwargs)
        self.__test_dir = os.path.join(self._test_dir, 'test_gin')
        self.__gin_mako_dir = os.path.join(self._mako_dir, 'go', 'gin')

        self.__api_package_name = os.path.basename(self.__api_dir)
        self.__define_dir = kwargs['go_gin_define_dir']
        self.__package_define = tool.package_name(self.__define_dir, self.go_src_dir)
        self.__package_api = tool.package_name(self.__api_dir, self.go_src_dir)

    def gen_code(self):
        self.gen_api()
        self.gen_test()
        self.gen_define()
        self.gen_router()
        self.gen_init()

    def gen_api(self):
        mako_file = os.path.join(self.__gin_mako_dir, 'api.go')
        for api in self.protocol.apis:
            filename = "%s.go" % api.name
            filename = os.path.join(self.__api_dir, filename)
            if not os.path.exists(filename):
                tool.gen_code_file(mako_file, filename,
                                   api=api,
                                   package_name=self.__api_package_name,
                                   package_go_gin_define=self.__package_define,
                                   package_module_dir=self.package_module_dir,
                                   gen_lower_camel=util.gen_lower_camel,
                                   go_gin_define_dir=self.__define_dir,
                                   json_output=tool.dict2json(api.resp.value_map),
                                   )

    def gen_test(self):
        self.init_test(self.__test_dir)
        mako_file = os.path.join(self.__gin_mako_dir, 'test.go')
        for api in self.protocol.apis:
            filename = "%s_test.go" % util.gen_upper_camel(api.name)
            filename = os.path.join(self.__test_dir, filename)
            input_text = tool.dict2json(api.req.value_map)
            tool.gen_code_file(mako_file, filename,
                               api=api,
                               input_text=input_text,
                               package_module_dir=self.package_module_dir,
                               module_dir=self.module_dir,
                               url_param2text=tool.url_param2text,
                               gen_upper_camel=util.gen_upper_camel,
                               )

    def gen_define(self):
        out_file = os.path.join(self.__define_dir, 'define.go')
        mako_file = os.path.join(self.__gin_mako_dir, 'define.go')
        tool.gen_code_file(mako_file,
                           out_file,
                           package_name=os.path.basename(self.__define_dir),
                           nodes=self.protocol.nodes,
                           enums=self.protocol.enums,
                           has_file=self.protocol.has_file,
                           has_time=self.protocol.has_time,
                           gen_upper_camel=util.gen_upper_camel,
                           )

    def gen_router(self):
        out_file = os.path.join(self.__api_dir, "router.go")
        mako_file = os.path.join(self.__gin_mako_dir, 'router.go')
        tool.gen_code_file(mako_file,
                           out_file,
                           package_name=self.__api_package_name,
                           package_define=self.__package_define,
                           package_module_dir=self.package_module_dir,
                           apis=self.protocol.apis,
                           gen_lower_camel=util.gen_lower_camel,
                           # has_file=self.protocol.has_file,
                           # has_time=self.protocol.has_time,
                           )

    def gen_init(self):
        out_file = os.path.join(self.module_dir, 'cmd', 'init_gin.go')
        mako_file = os.path.join(self.__gin_mako_dir, 'init.go')
        # if not os.path.exists(out_file):
        tool.gen_code_file(mako_file,
                           out_file,
                           package_api=self.__package_api,
                           package_module_dir=self.package_module_dir,
                           )
