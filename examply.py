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
                "json/api.json",
                "json/api_url.json",
                ],
            code_type='go',
            project_dir=dst_dir,
            # project_start_dir=dst_dir,
            go_module='example',
            service_name="example",
            mako_dir="/home/ubuntu/gencode/mako",
            main_dir=os.path.join(dst_dir, "cmd"),
            error_package="example/app/errno",
            # graphql_define_package="graphql_define",
            graphql_define_dir=os.path.join(dst_dir, "app", "graphql_api", "graphql_define"),
            graphql_api_dir=os.path.join(dst_dir, "app", "graphql_api"),
            graphql_resolver_dir=os.path.join(dst_dir, "app", "graphql_api", "graphql_resolver"),
            graphql_resolver_type="GraphqlResolver",
            restful_api_dir=os.path.join(dst_dir, "app", "restful_api"),
            restful_define_dir=os.path.join(dst_dir, 'app', 'restful_api', "restful_define"),
            restful_define_package="restful_define",
            restful_api_package="restful_api",
            grpc_proto_dir=os.path.join(dst_dir, "grpc_pb"),
            private_grpc_proto_dir=os.path.join(dst_dir, "private_grpc_pb"),
            grpc_api_dir=os.path.join(dst_dir, "app", "grpc_api"),
            grpc_service_name="GrpcExampleServer",
            grpc_service_type="Server",
            proto_package="protopb",
            grpc_package="grpc_pb",
            # grpc_define_pkg_name="define",
            gen_server=True,
            gen_client=None,
            gen_test=True,
            gen_doc=True,
            gen_out=False,
            )
