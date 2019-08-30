#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# from mako.template import Template
import util
from gencode.common import tool
# import copy


def gen_apis_file(mako_file, output_dir, apis, project_start_dir, **kwargs):
    for api in apis:
        filename = "%s.go" % util.gen_underline_name(api.name)
        filename = os.path.join(output_dir, filename)
        if not os.path.exists(filename):
            tool.gen_code_file(mako_file, filename,
                               api=api,
                               package_restful_define_dir=tool.package_name(kwargs['restful_define_dir'], project_start_dir),
                               **kwargs)
    tool.go_fmt(output_dir)


def gen_tests_file(mako_file, output_dir, project_start_dir, apis, **kwargs):
    for api in apis:
        filename = "%s_test.go" % util.gen_upper_camel(api.name)
        filename = os.path.join(output_dir, filename)
        kwargs['json_input'] = tool.dict2json(api.req.value)
        tool.gen_code_file(mako_file, filename,
                           api=api,
                           **kwargs)
    tool.go_fmt(output_dir)


def gen_defines_file(mako_file, output_dir, apis, nodes, project_start_dir, **kwargs):
    for node in nodes:
        filename = "%s.go" % node.type.name
        filename = os.path.join(output_dir, filename)
        tool.gen_code_file(mako_file, filename,
                           node=node,
                           **kwargs)
    tool.go_fmt(output_dir)


def gen_code_file(mako_dir, gen_server, gen_client, gen_test, gen_doc, **kwargs):

    mako_dir = os.path.join(mako_dir, 'go', 'restful')

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
                           package_restful_api_dir=tool.package_name(kwargs['restful_api_dir'], kwargs['project_start_dir']),
                           package_restful_define_dir=tool.package_name(kwargs['restful_define_dir'], kwargs['project_start_dir']),
                           package_project_dir=tool.package_name(kwargs['project_dir'], kwargs['project_start_dir']),
                           **kwargs)
        tool.go_fmt(out_file)

        # define
        gen_defines_file(os.path.join(mako_dir, 'define.go'),
                         kwargs['restful_define_dir'],
                         package_project_dir=tool.package_name(kwargs['project_dir'], kwargs['project_start_dir']),
                         **kwargs)

        # apis
        gen_apis_file(os.path.join(mako_dir, 'api.go'),
                      kwargs['restful_api_dir'],
                      package_project_dir=tool.package_name(kwargs['project_dir'], kwargs['project_start_dir']),
                      **kwargs)

        # init_restful
        out_file = os.path.join(kwargs['project_dir'], 'cmd', 'init_restful.go')
        # if not os.path.exists(out_file):
        tool.gen_code_file(os.path.join(mako_dir, 'init_restful.go'),
                           out_file,
                           package_restful_api_dir=tool.package_name(kwargs['restful_api_dir'], kwargs['project_start_dir']),
                           package_project_dir=tool.package_name(kwargs['project_dir'], kwargs['project_start_dir']),
                           **kwargs,
                           )
        tool.go_fmt(out_file)

    if gen_test:
        # test
        gen_tests_file(os.path.join(mako_dir, 'test.go'),
                       os.path.join(kwargs['restful_api_dir'], 'test_restful'),
                       **kwargs)
