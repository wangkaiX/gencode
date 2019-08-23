#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from gencode.common import gen

if __name__ == '__main__':
    gopath = os.environ['GOPATH']
    assert gopath
    dst_dir = os.environ['GOPATH'] + "/src/example"  # env['GOPATH'] + "/src/"
    gen.gen_code_files(
            filenames=[
                "json/api_url.json",
                "json/api.json",
                ],
            code_type='go',
            project_dir=dst_dir,
            project_start_dir=dst_dir,
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
            restful_api_dir=os.path.join(dst_dir, "app", "restful_api"),
            restful_define_dir=os.path.join(dst_dir, 'app', 'restful_api', "restful_define"),
            restful_define_package_name="restful_define",
            restful_api_package_name="restful_api",
            grpc_proto_dir=os.path.join(dst_dir, "grpc_pb"),
            grpc_api_dir=os.path.join(dst_dir, "app", "grpc_api"),
            grpc_service_name="GrpcExampleServer",
            grpc_service_type_name="Server",
            proto_package_name="protopb",
            grpc_package_name="grpc_pb",
            # grpc_define_pkg_name="define",
            gen_server=True,
            gen_client=None,
            gen_test=True,
            gen_doc=True,
            )
