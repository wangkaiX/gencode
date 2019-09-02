#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# import shutil
from gencode.common import parser_config
import util
from gencode.common import tool
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
            project_dir,
            # service_name,
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
            restful_define_dir=None,
            grpc_proto_dir=None,
            grpc_service_name=None,
            grpc_service_type=None,
            # grpc_service_dir=None,
            grpc_package=None,
            proto_package=None,
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
    # assert service_name
    assert mako_dir

    apis, protocol, configs, config_map = parser_config.gen_apis(filename)
    if protocol.type == meta.proto_graphql:
        assert graphql_dir and \
               graphql_schema_dir and \
               graphql_define_pkg_name and \
               graphql_resolver_pkg_name
    elif protocol.type == meta.proto_http:
        assert restful_api_dir and \
               restful_define_dir
    elif protocol.type == meta.proto_grpc:
        assert grpc_proto_dir and \
               grpc_api_dir and \
               grpc_service_name and \
               grpc_service_type and \
               grpc_package and \
               proto_package
    else:
        print("未知的协议[%s]" % protocol)
        assert False

    return apis, protocol, configs, config_map


def __gen_code_file(
            filename,
            code_type,
            **kwargs,
            ):
    print("file:", filename)
    meta.Node.clear()
    meta.Enum.clear()
    apis, protocol, configs, config_map = check_args(filename, code_type, **kwargs)

    nodes = meta.Node.req_resp_nodes()
    types = set([node.type.name for node in nodes])
    unique_nodes = []
    for node in nodes:
        if node.type.name in types:
            unique_nodes.append(node)
            types.remove(node.type.name)

    kwargs['nodes'] = unique_nodes
    kwargs['enums'] = meta.Enum.enums()
    kwargs['apis'] = apis
    kwargs['protocols'].append(protocol)
    kwargs['configs'] += configs
    kwargs['config_map'] = dict(kwargs['config_map'], **config_map)

    # print("config_map:", kwargs['config_map'])

    if code_type in meta.code_go:
        if protocol.type == meta.proto_grpc:
            go_grpc_gen.gen_code_file(**kwargs)
        elif protocol.type == meta.proto_http:
            go_restful_gen.gen_code_file(**kwargs)
    elif code_type in meta.code_cpp:
        pass
    else:
        print("不支持的语言[%s]" % (code_type))
        assert False
    return protocol, kwargs['configs'], kwargs['config_map']


def gen_code_files(filenames, code_type, **kwargs):
    kwargs['protocols'] = []
    kwargs['configs'] = []
    kwargs['config_map'] = {}
    kwargs['gen_upper_camel'] = util.gen_upper_camel
    kwargs['gen_lower_camel'] = util.gen_lower_camel
    kwargs['gen_underline_name'] = util.gen_underline_name
    code_type = code_type.upper()
    kwargs['mako_dir'] = util.abs_path(kwargs['mako_dir'])
    for filename in filenames:
        protocol, configs, config_map = __gen_code_file(filename, code_type, **kwargs)
        kwargs['configs'] = configs
        kwargs['config_map'] = config_map

    if code_type in meta.code_go:
        # config.toml
        output_file = os.path.join(kwargs['project_dir'], 'configs', 'config.toml')
        tool.gen_code_file(os.path.join(kwargs['mako_dir'], 'go', 'config.toml'),
                           output_file,
                           **kwargs,
                           )

        # config.go
        # print("configs:", configs)
        # print("config_map:", config_map)
        output_file = os.path.join(kwargs['project_dir'], 'app', 'define', 'config.go')
        tool.gen_code_file(os.path.join(kwargs['mako_dir'], 'go', 'config.go'),
                           output_file,
                           **kwargs,
                           )
        # main
        out_file = os.path.join(kwargs['project_dir'], 'cmd', 'main.go')
        tool.gen_code_file(os.path.join(kwargs['mako_dir'], 'go', 'main.go'),
                           out_file,
                           package_project_dir=kwargs['go_module'],
                           **kwargs)
        tool.go_fmt(out_file)
    else:
        print("不支持的语言[%s]" % (code_type))
        assert False
