#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# from mako.template import Template
import util
from gencode.common import meta
from gencode.common import tool
import copy


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


def gen_pb_file(make_dir):
    os.chdir(make_dir)
    os.system("make")


def gen_tests_file(mako_file, output_dir, grpc_proto_dir, project_start_path, apis, **kwargs):
    for api in apis:
        filename = "%s_test.go" % util.gen_underline_name(api.name)
        filename = os.path.join(output_dir, filename)
        kwargs['grpc_proto_dir'] = tool.package_name(grpc_proto_dir, project_start_path)
        kwargs['json_input'] = tool.dict2json(api.req.value)
        tool.gen_code_file(mako_file, filename,
                           api=api,
                           **kwargs)
    tool.go_fmt(output_dir)


def gen_code_file(mako_dir, gen_server, gen_client, gen_test, gen_doc, **kwargs):
    nodes = meta.Node.all_nodes()
    types = set([node.type.name for node in nodes])
    unique_nodes = []
    for node in nodes:
        if node.type.name in types:
            unique_nodes.append(node)
            types.remove(node.type.name)

    kwargs['nodes'] = unique_nodes
    kwargs['enums'] = meta.Enum.enums()
    kwargs['gen_upper_camel'] = util.gen_upper_camel
    kwargs['gen_lower_camel'] = util.gen_lower_camel
    kwargs['gen_underline_name'] = util.gen_underline_name

    mako_dir = os.path.join(mako_dir, 'go', 'grpc')

    # proto
    tool.gen_code_file(os.path.join(mako_dir, 'grpc.proto'),
                       os.path.join(kwargs['grpc_proto_dir'], '%s.proto' % kwargs['proto_package_name']), **kwargs)

    # makefile
    tool.gen_code_file(os.path.join(mako_dir, 'proto.mak'),
                       os.path.join(kwargs['grpc_proto_dir'], 'makefile'), **kwargs)

    # pb.go
    gen_pb_file(make_dir=kwargs['grpc_proto_dir'])

    if gen_server:
        # service_define
        tool.gen_code_file(os.path.join(mako_dir, 'service_define.go'),
                           os.path.join(kwargs['grpc_api_dir'],
                                        "%s.go" % util.gen_underline_name(kwargs['grpc_service_type_name'])),
                           **kwargs)

        # apis
        gen_apis_file(os.path.join(mako_dir, 'api.go'),
                      kwargs['grpc_api_dir'], **kwargs)

        # init_grpc
        output_file = os.path.join(kwargs['project_path'], 'cmd', 'init_grpc.go')
        if not os.path.exists(output_file):
            tempargs = copy.deepcopy(kwargs)
            tempargs['grpc_api_dir'] = tool.package_name(kwargs['grpc_api_dir'], kwargs['project_start_path'])
            tempargs['grpc_proto_dir'] = tool.package_name(kwargs['grpc_proto_dir'], kwargs['project_start_path'])
            tool.gen_code_file(os.path.join(mako_dir, 'init_grpc.go'),
                               output_file,
                               **tempargs,
                               )

    if gen_test:
        # test
        gen_tests_file(os.path.join(mako_dir, 'test.go'),
                       os.path.join(kwargs['grpc_api_dir'], 'test_grpc'),
                       **kwargs)
