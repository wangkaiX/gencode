#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from gencode.common import gen

if __name__ == '__main__':
    gopath = os.environ['GOPATH']
    assert gopath
    dst_dir = os.environ['GOPATH'] + "/src/example"  # env['GOPATH'] + "/src/"
    gen.gen_code(
            filenames=[
                "json/newVersion3.json",
                ],
            code_type='go',
            project_path=dst_dir,
            service_name="example",
            mako_dir="~/gencode/mako",
            main_dir=os.path.join(dst_dir, "cmd"),
            error_package="example/app/errno",
            # graphql_dir=os.path.join(dst_dir, "app"," graphql_api"),
            # graphql_schema_dir="custom",
            # graphql_define_pkg_name="custom",
            # graphql_resolver_pkg_name="custom",
            # graphql_ip="",
            # graphql_port=49001,
            # restful_dir=dst_dir + "app/restful_api",
            # restful_define_pkg_name="custom",
            # restful_resolver_pkg_name="custom",
            # restful_ip="",
            # restful_port=49002,
            grpc_proto_dir=os.path.join(dst_dir, "grpc_pb"),
            grpc_api_dir=os.path.join(dst_dir, "app", "grpc_api"),
            grpc_service_name="Server",
            # grpc_service_dir=os.path.join(dst_dir, 'app', 'grpc_api'),
            proto_package_name="protopb",
            grpc_package_name="grpc_pb",
            # grpc_define_pkg_name="define",
            grpc_ip="0.0.0.0",
            grpc_port=49003,
            gen_server=True,
            gen_client=None,
            gen_test=None,
            )
