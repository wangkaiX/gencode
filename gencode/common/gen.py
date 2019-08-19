#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# import shutil
from gencode.common import parser_config
import util
from gencode.common import meta
from gencode.go.grpc import gen as go_grpc_gen
from gencode.go.restful import gen as go_restful_gen
# from gencode import cpp


def gen_server():
    pass


def gen_client():
    pass


def gen_test():
    pass


def save_file(filename, txt):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filename, 'w') as f:
        f.write(txt)


def go_fmt(filename):
    cmd = "go fmt %s" % filename
    os.system(cmd)


def check_args(
            filename,
            code_type,
            project_path,
            project_start_path,
            service_name,
            main_dir,
            mako_dir,
            error_package,
            graphql_dir=None,
            graphql_schema_dir=None,
            graphql_define_pkg_name=None,
            graphql_resolver_pkg_name=None,
            graphql_ip=None,
            graphql_port=None,
            restful_api_dir=None,
            restful_package_name=None,
            restful_ip=None,
            restful_port=None,
            grpc_proto_dir=None,
            grpc_service_name=None,
            grpc_service_type_name=None,
            # grpc_service_dir=None,
            grpc_package_name=None,
            proto_package_name=None,
            grpc_api_dir=None,
            # grpc_define_pkg_name="Server",
            grpc_ip=None,
            grpc_port=None,
            # gen_server=None,
            # gen_client=None,
            # gen_test=None,
            **kwargs,
            ):
    assert code_type
    code_type = code_type.upper()
    assert gen_server or gen_client or gen_test
    if code_type not in meta.code_go + meta.code_cpp:
        print("不支持的语言[%s]" % code_type)
    assert service_name
    assert mako_dir

    apis, protocol = parser_config.gen_apis(filename)
    protocol = protocol.upper()
    if protocol == meta.proto_graphql:
        assert graphql_dir and \
               graphql_schema_dir and \
               graphql_define_pkg_name and \
               graphql_resolver_pkg_name and \
               graphql_ip and graphql_port
    elif protocol == meta.proto_http:
        assert restful_api_dir and \
               restful_package_name and \
               restful_ip and \
               restful_port
    elif protocol == meta.proto_grpc:
        assert grpc_proto_dir and \
               grpc_api_dir and \
               grpc_ip and \
               grpc_port and \
               grpc_service_name and \
               grpc_service_type_name and \
               grpc_package_name and \
               proto_package_name
    else:
        assert False and "未知的协议[%s]" % protocol

    return apis, protocol


def gen_code_file(
            filename,
            code_type,
            **kwargs,
            ):
    apis, protocol = check_args(filename, code_type, **kwargs)
    kwargs['mako_dir'] = util.abs_path(kwargs['mako_dir'])
    code_type = code_type.upper()

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
    kwargs['apis'] = apis

    if code_type in meta.code_go:
        if protocol == meta.proto_grpc:
            go_grpc_gen.gen_code_file(**kwargs)
        elif protocol == meta.proto_http:
            go_restful_gen.gen_code_file(**kwargs)
    elif code_type in meta.code_cpp:
        pass
    else:
        print("不支持的语言[%s]" % (code_type))
        assert False


def gen_code_files(filenames, code_type, **kwargs):
    for filename in filenames:
        gen_code_file(filename, code_type, **kwargs)
