#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# from mako.template import Template
import util.python.util as util
from src.common import tool
from src.go.base.go_common_generator_base import GoCommonGeneratorBase
# import copy


class GoGin(GoCommonGeneratorBase):
    def __init__(self, protocol, **kwargs):
        GoCommonGeneratorBase.__init__(self, protocol, **kwargs)
        self.__api_dir = kwargs['go_gin_api_dir']
        self.__test_dir = os.path.join(self.__api_dir, 'test_gin')

        self.__api_package_name = os.path.basename(self.__api_dir)
        self.__define_dir = kwargs['go_gin_define_dir']
        self.__package_define = tool.package_name(self.__define_dir, self.go_src_dir)
        self.__package_api = tool.package_name(self.__api_dir, self.go_src_dir)

    def gen_code(self):
        GoCommonGeneratorBase.gen_code(self)
        self.gen_api()
        self.gen_test()
        self.gen_define()
        self.gen_router()
        self.gen_init()

    def gen_api(self):
        mako_file = os.path.join(self.mako_dir, 'go', 'gin', 'api.go')
        for api in self.protocol.apis:
            filename = "%s.go" % api.name
            filename = os.path.join(self.__api_dir, filename)
            if not os.path.exists(filename):
                tool.gen_code_file(mako_file, filename,
                                   api=api,
                                   package_name=self.__api_package_name,
                                   package_go_gin_define=self.__package_define,
                                   package_service=self.package_service,
                                   gen_lower_camel=util.gen_lower_camel,
                                   go_gin_define_dir=self.__define_dir,
                                   json_output=tool.dict2json(api.resp.value_map),
                                   )

    def gen_test(self):
        mako_file = os.path.join(self.mako_dir, 'go', 'gin', 'test.go')
        for api in self.protocol.apis:
            filename = "%s_test.go" % util.gen_upper_camel(api.name)
            filename = os.path.join(self.__test_dir, filename)
            input_text = tool.dict2json(api.req.value_map)
            tool.gen_code_file(mako_file, filename,
                               api=api,
                               input_text=input_text,
                               package_service=self.package_service,
                               service_dir=self.service_dir,
                               url_param2text=tool.url_param2text,
                               gen_upper_camel=util.gen_upper_camel,
                               )

    def gen_define(self):
        out_file = os.path.join(self.__define_dir, 'define.go')
        mako_file = os.path.join(self.mako_dir, 'go', 'gin', 'define.go')
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
        mako_file = os.path.join(self.mako_dir, 'go', 'gin', 'router.go')
        tool.gen_code_file(mako_file,
                           out_file,
                           package_name=self.__api_package_name,
                           package_define=self.__package_define,
                           package_service=self.package_service,
                           apis=self.protocol.apis,
                           gen_lower_camel=util.gen_lower_camel,
                           # has_file=self.protocol.has_file,
                           # has_time=self.protocol.has_time,
                           )

    def gen_init(self):
        out_file = os.path.join(self.service_dir, 'cmd', 'init_gin.go')
        mako_file = os.path.join(self.mako_dir, 'go', 'gin', 'init.go')
        # if not os.path.exists(out_file):
        tool.gen_code_file(mako_file,
                           out_file,
                           package_api=self.__package_api,
                           package_service=self.package_service,
                           )
