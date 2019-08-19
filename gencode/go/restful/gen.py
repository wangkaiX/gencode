#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# from mako.template import Template
import util
from gencode.common import tool
# import copy


def gen_apis_file(mako_file, output_dir, apis, grpc_api_dir, grpc_proto_dir, project_start_path, **kwargs):
    for api in apis:
        filename = "%s.go" % util.gen_underline_name(api.name)
        filename = os.path.join(output_dir, filename)
        if not os.path.exists(filename):
            tool.gen_code_file(mako_file, filename,
                               api=api,
                               grpc_api_dir=tool.package_name(grpc_api_dir, project_start_path),
                               grpc_proto_dir=tool.package_name(grpc_proto_dir, project_start_path),
                               **kwargs)
    tool.go_fmt(output_dir)


def gen_tests_file(mako_file, output_dir, grpc_proto_dir, project_start_path, apis, **kwargs):
    for api in apis:
        filename = "%s_test.go" % util.gen_upper_camel(api.name)
        filename = os.path.join(output_dir, filename)
        kwargs['grpc_proto_dir'] = tool.package_name(grpc_proto_dir, project_start_path)
        kwargs['json_input'] = tool.dict2json(api.req.value)
        tool.gen_code_file(mako_file, filename,
                           api=api,
                           **kwargs)
    tool.go_fmt(output_dir)


def gen_code_file(mako_dir, gen_server, gen_client, gen_test, gen_doc, **kwargs):

    mako_dir = os.path.join(mako_dir, 'go', 'restful')

    if gen_server:
        # router
        tool.gen_code_file(os.path.join(mako_dir, 'router.go'),
                           os.path.join(kwargs['restful_api_dir'], "router.go"), **kwargs)

        # apis
        gen_apis_file(os.path.join(mako_dir, 'api.go'),
                      kwargs['restful_api_dir'], **kwargs)

        # init_restful
        output_file = os.path.join(kwargs['project_path'], 'cmd', 'init_restful.go')
        if not os.path.exists(output_file):
            tool.gen_code_file(os.path.join(mako_dir, 'init_grpc.go'),
                               output_file,
                               package_restful_api_dir=tool.package_name(kwargs['restful_api_dir'], kwargs['project_start_path']),
                               package_project_dir=tool.package_name(kwargs['project_path'], kwargs['project_start_path']),
                               **kwargs,
                               )

    if gen_test:
        # test
        gen_tests_file(os.path.join(mako_dir, 'test.go'),
                       os.path.join(kwargs['restful_api_dir'], 'test_restful'),
                       **kwargs)
