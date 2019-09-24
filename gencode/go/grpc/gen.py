#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# import copy
# from mako.template import Template
import util
from gencode.common import tool
from gencode.common import meta
# import copy


def gen_apis_file(mako_file, output_dir, apis, grpc_api_dir, grpc_proto_dir, go_module, **kwargs):
    for api in apis:
        filename = "%s.go" % util.gen_underline_name(api.name)
        filename = os.path.join(output_dir, filename)
        if not os.path.exists(filename):
            tool.gen_code_file(mako_file, filename,
                               api=api,
                               package_grpc_api_dir=tool.package_name(grpc_api_dir, go_module),
                               package_grpc_proto_dir=tool.package_name(grpc_proto_dir, go_module),
                               **kwargs)
    tool.go_fmt(output_dir)


def gen_pb_file(make_dir):
    old_path = os.path.abspath('.')
    os.chdir(make_dir)
    r = os.popen("make")
    r.read()
    # os.system("make")
    os.chdir(old_path)


def gen_tests_file(mako_file, output_dir, grpc_proto_dir, go_module, apis, **kwargs):
    for api in apis:
        filename = "%s_test.go" % util.gen_upper_camel(api.name)
        filename = os.path.join(output_dir, filename)
        tool.gen_code_file(mako_file, filename,
                           api=api,
                           package_grpc_proto_dir=tool.package_name(grpc_proto_dir, go_module),
                           json_input=tool.dict2json(api.req.value),
                           **kwargs)
    tool.go_fmt(output_dir)


def gen_pb(mako_dir, grpc_proto_dir, **kwargs):
    # proto
    util.assert_file(os.path.join(mako_dir, 'grpc.proto'))
    tool.gen_code_file(os.path.join(mako_dir, 'grpc.proto'),
                       os.path.join(grpc_proto_dir, '%s.proto' % kwargs['proto_package']), **kwargs)

    # makefile
    tool.gen_code_file(os.path.join(mako_dir, 'proto.mak'),
                       os.path.join(grpc_proto_dir, 'makefile'), **kwargs)

    # pb.go
    gen_pb_file(make_dir=grpc_proto_dir)


def gen_code_file(mako_dir, gen_server, gen_client, gen_test, gen_doc, **kwargs):

    # add code msg
    # for api in kwargs['apis']:
    #     api.resp.add_field(meta.field_code)
    #     api.resp.add_field(meta.field_msg)

    mako_dir = os.path.join(mako_dir, 'go', 'grpc')

    # proto
    gen_pb(mako_dir, **kwargs)

    # private proto
    private_kwargs = kwargs.copy()
    private_kwargs['apis'] = [api for api in private_kwargs['apis'] if api.api_tag == meta.public]
    private_kwargs['grpc_proto_dir'] = private_kwargs['private_grpc_proto_dir']
    gen_pb(mako_dir, **private_kwargs)

    if gen_server:
        # service_define
        tool.gen_code_file(os.path.join(mako_dir, 'service_define.go'),
                           os.path.join(kwargs['grpc_api_dir'],
                                        "%s.go" % util.gen_underline_name(kwargs['grpc_service_type'])),
                           **kwargs)

        # check_args
        tool.gen_code_file(os.path.join(mako_dir, 'check_args.go'),
                           os.path.join(kwargs['grpc_api_dir'], 'check_args.go'),
                           package_grpc_api_dir=tool.package_name(kwargs['grpc_api_dir'], kwargs['go_module']),
                           package_grpc_proto_dir=tool.package_name(kwargs['grpc_proto_dir'], kwargs['go_module']),
                           **kwargs,
                           )

        # apis
        gen_apis_file(os.path.join(mako_dir, 'api.go'),
                      kwargs['grpc_api_dir'], **kwargs)

        # init_grpc
        output_file = os.path.join(kwargs['project_dir'], 'cmd', 'init_grpc.go')
        # if not os.path.exists(output_file):
        tool.gen_code_file(os.path.join(mako_dir, 'init_grpc.go'),
                           output_file,
                           package_grpc_api_dir=tool.package_name(kwargs['grpc_api_dir'], kwargs['go_module']),
                           package_grpc_proto_dir=tool.package_name(kwargs['grpc_proto_dir'], kwargs['go_module']),
                           package_project_dir=kwargs['go_module'],
                           **kwargs,
                           )

    if gen_test:
        # test
        gen_tests_file(os.path.join(mako_dir, 'test.go'),
                       os.path.join(kwargs['grpc_api_dir'], 'test_grpc'),
                       **kwargs)
