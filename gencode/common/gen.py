#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# import shutil
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
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filename, 'w') as f:
        f.write(txt)


def gen_code(
            filenames,
            code_type,
            project_path,
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
            restful_dir=None,
            restful_define_pkg_name=None,
            # restful_service_define_name="Server",
            restful_resolver_pkg_name=None,
            restful_ip=None,
            restful_port=None,
            grpc_proto_dir=None,
            grpc_service_name=None,
            grpc_service_dir=None,
            grpc_package_name=None,
            proto_package_name=None,
            grpc_pb_dir=None,
            grpc_define_pkg_name="Server",
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
    assert service_name
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
        code_proto, code_service_define, code_apis = \
            go_grpc_gen.gen_code(project_path=project_path, apis=proto_apis, mako_dir=mako_dir,
                                 proto_service_name=service_name,
                                 proto_package_name=proto_package_name,
                                 grpc_package_name=grpc_package_name,
                                 grpc_service_name=grpc_service_name,
                                 error_package=error_package)

        # proto
        filename = "%s.proto" % util.gen_underline_name(service_name)
        filename = os.path.join(grpc_proto_dir, filename)
        print(code_proto)
        save_file(filename, code_proto)

        # pb
        filename = "%s.go" % util.gen_underline_name(grpc_service_name)
        filename = os.path.join(grpc_pb_dir, filename)
        save_file(filename, code_service_define)

        for k, v in code_apis.items():
            filename = "%s.go" % util.gen_underline_name(k)
            filename = os.path.join(grpc_pb_dir, filename)
            save_file(filename, v)

    elif code_type in meta.code_cpp:
        pass
    else:
        print("不支持的语言[%s]" % (code_type))
        assert False