#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from gencode.common import parser_config
import util
from gencode.common import meta
from gencode.go.grpc import gen as go_grpc_gen
# from gencode import cpp


def gen_server():
    pass


def gen_client():
    pass


def gen_test():
    pass


def save_file(filename, txt):
    with open(filename, 'w') as f:
        f.write(txt)


def gen_code(
            filenames,
            code_type,
            project_name,
            mako_dir=None,
            graphql_dir=None,
            graphql_schema_dir=None,
            graphql_define_pkg_name=None,
            graphql_resolver_pkg_name=None,
            graphql_ip=None,
            graphql_port=None,
            restful_dir=None,
            restful_define_pkg_name=None,
            restful_resolver_pkg_name=None,
            restful_ip=None,
            restful_port=None,
            grpc_proto_dir=None,
            grpc_pb_dir=None,
            grpc_define_pkg_name=None,
            grpc_ip=None,
            grpc_port=None,
            gen_server=None,
            gen_client=None,
            gen_test=None,
            ):
    assert code_type
    code_type = code_type.upper()
    assert gen_server or gen_client or gen_test
    if code_type not in meta.code_go + meta.code_cpp:
        print("不支持的语言[%s]" % code_type)
    assert project_name
    assert mako_dir
    mako_dir = util.abs_path(mako_dir)

    graphql_apis = []
    restful_apis = []
    proto_apis = []
    for filename in filenames:
        apis = parser_config.gen_apis(filename)
        for api in apis:
            for protocol in api.protocols:
                if protocol.protocol == meta.proto_graphql:
                    assert graphql_dir and \
                           graphql_schema_dir and \
                           graphql_define_pkg_name and \
                           graphql_resolver_pkg_name and \
                           graphql_ip and graphql_port
                    graphql_apis.append(api)
                if protocol.protocol == meta.proto_http:
                    assert restful_dir and \
                           restful_define_pkg_name and \
                           restful_resolver_pkg_name and \
                           restful_ip and \
                           restful_port
                    restful_apis.append(api)
                if protocol.protocol == meta.proto_proto:
                    assert grpc_proto_dir and \
                           grpc_pb_dir and \
                           grpc_define_pkg_name and \
                           grpc_ip and \
                           grpc_port
                    proto_apis.append(api)

    if code_type in meta.code_go:
        code_proto = go_grpc_gen.gen_code(proto_apis, mako_dir)
        filename = "%s.pb.go" % project_name
        filename = os.path.join(grpc_proto_dir, filename)
        print(code_proto)
        save_file(filename, code_proto)
    elif code_type in meta.code_cpp:
        pass
    else:
        print("不支持的语言[%s]" % (code_type))
        assert False
