#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from gencode.common import gen

if __name__ == '__main__':
    go_path = os.environ['GOPATH']
    go_src = os.path.join(go_path, "src")
    dst_dir = os.path.join(go_src, "example")  # env['GOPATH'] + "/src/"
    gen.gen_code_files(
            filenames=[
                os.path.join("json", "api.json"),
                os.path.join("json", "api_url.json"),
                ],
            error_config_file="json/errno.config",
            error_out_dir=os.path.join(dst_dir, "app", "errno"),
            errno_begin=10000,
            errno_end=20000,

            code_type='go',
            project_dir=dst_dir,
            # project_start_dir=dst_dir,
            go_src=go_src,
            # service_name="example",
            mako_dir=os.path.join("E:/", "gencode", "mako"),
            # mako_dir="E:gencode\\mako",
            main_dir=os.path.join(dst_dir, "cmd"),
            # error_package="example/app/errno",
            # graphql_define_package="graphql_define",
            graphql_define_dir=os.path.join(dst_dir, "app", "graphql_api", "graphql_define"),
            graphql_api_dir=os.path.join(dst_dir, "app", "graphql_api"),
            graphql_resolver_dir=os.path.join(dst_dir, "app", "graphql_api", "graphql_resolver"),
            graphql_resolver_type="GraphqlResolver",

            restful_api_dir=os.path.join(dst_dir, "app", "restful_api"),
            restful_define_dir=os.path.join(dst_dir, 'app', 'restful_api', "restful_define"),
            # restful_define_package="restful_define",
            # restful_api_package="restful_api",
            grpc_proto_dir=os.path.join(dst_dir, "grpc_pb"),
            # private_grpc_proto_dir=os.path.join(dst_dir, "private_grpc_pb"),
            grpc_api_dir=os.path.join(dst_dir, "app", "grpc_api"),
            grpc_service_name="GrpcExampleServer",
            grpc_service_type="Server",
            proto_package="protopb",
            # grpc_package="grpc_pb",
            # grpc_define_pkg_name="define",
            gen_server=True,
            gen_client=None,
            gen_test=True,
            gen_doc=True,
            gen_out=False,
            )
