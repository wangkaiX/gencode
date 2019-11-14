#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# from mako.template import Template
import util.python.util as util
from src.common import tool
from src.go.gen_code import GoCode
# import copy


class GoGin(GoCode):
    def __init__(self, protocol, **kwargs):
        GoCode.__init__(self, protocol, **kwargs)
        self.__api_dir = kwargs['go_gin_api_dir']
        self.__test_dir = os.path.join(self.__api_dir, 'test_gin')

        self.__restful_api_package_name = os.path.basename(self.__api_dir)
        self.__go_gin_define_dir = tool.package_name(kwargs['go_gin_define_dir'])
        self.__package_go_gin_define = tool.package_name(self.__go_gin_define_dir, self.__go_src)

    def gen_code(self):
        GoCode.gen_code(self)

    def gen_api(self):
        mako_file = os.path.join(self.__mako_dir, 'go', 'gin', 'api.go')
        for api in self.__protocol.apis:
            filename = "%s.go" % api.name
            filename = os.path.join(self.__api_dir, filename)
            if not os.path.exists(filename):
                tool.gen_code_file(mako_file, filename,
                                   api=api,
                                   package_name=self.__restful_api_package_name,
                                   package_go_gin_define=self.__package_go_gin_define,
                                   package_project=self.__package_project
                                   )

    def gen_test(self):
        mako_file = os.path.join(self.__mako_dir, 'go', 'gin', 'test.go')
        for api in self.__protocol.apis:
            filename = "%s_test.go" % util.gen_upper_camel(api.name)
            filename = os.path.join(self.__test_dir, filename)
            input_text = tool.dict2json(api.req.value_map)
            tool.gen_code_file(mako_file, filename,
                               api=api,
                               input_text=input_text,
                               )

    def gen_define(self):
        out_file = os.path.join(kwargs['restful_define_dir'], 'restful_enum.go')
        mako_file = os.path.join(mako_dir, 'enum.go')
        tool.gen_code_file(os.path.join(mako_dir, 'enum.go'),
                           out_file,
                           **kwargs)



def gen_defines_file(mako_file, output_dir, apis, nodes, **kwargs):
    for node in nodes:
        filename = "%s.go" % node.type.name
        filename = os.path.join(output_dir, filename)
        tool.gen_code_file(mako_file, filename,
                           node=node,
                           # restful_define_package=os.path.basename(kwargs['restful_define_dir']),
                           **kwargs)
    tool.go_fmt(output_dir)


def gen_code_file(mako_dir, gen_server, gen_client, gen_test, gen_doc, **kwargs):

    # enum
    out_file = os.path.join(kwargs['restful_define_dir'], 'restful_enum.go')
    tool.gen_code_file(os.path.join(mako_dir, 'enum.go'),
                       out_file,
                       **kwargs)

    if gen_server:
        # router
        out_file = os.path.join(kwargs['restful_api_dir'], "router.go")
        tool.gen_code_file(os.path.join(mako_dir, 'router.go'),
                           out_file,
                           package_restful_api_dir=tool.package_name(kwargs['restful_api_dir'], kwargs['go_src']),
                           package_restful_define_dir=tool.package_name(kwargs['restful_define_dir'], kwargs['go_src']),
                           package_project_dir=tool.package_name(kwargs['project_dir'], kwargs['go_src']),
                           **kwargs)
        tool.go_fmt(out_file)

        # define
        gen_defines_file(os.path.join(mako_dir, 'define.go'),
                         kwargs['restful_define_dir'],
                         package_project_dir=tool.package_name(kwargs['project_dir'], kwargs['go_src']),
                         **kwargs)

        # apis
        # gen_apis_file(os.path.join(mako_dir, 'api.go'),
        #               kwargs['restful_api_dir'],
        #               package_project_dir=tool.package_name(kwargs['project_dir'], kwargs['go_src']),
        #               **kwargs)

        # init_restful
        out_file = os.path.join(kwargs['project_dir'], 'cmd', 'init_restful.go')
        # if not os.path.exists(out_file):
        tool.gen_code_file(os.path.join(mako_dir, 'init_restful.go'),
                           out_file,
                           package_restful_api_dir=tool.package_name(kwargs['restful_api_dir'], kwargs['go_src']),
                           package_project_dir=tool.package_name(kwargs['project_dir'], kwargs['go_src']),
                           **kwargs,
                           )

    if gen_test:
        # test
        # gen_tests_file(os.path.join(mako_dir, 'test.go'),
        #                os.path.join(kwargs['restful_api_dir'], 'test_restful'),
        #                **kwargs)
