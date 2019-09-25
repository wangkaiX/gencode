#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from gencode.common import gen

if __name__ == '__main__':
    gopath = os.environ['GOPATH']
    assert gopath
    dst_dir = os.environ['GOPATH'] + "/src/example"  # env['GOPATH'] + "/src/"
    gen.gen_code_files(
            # 接口配置文件路径
            filenames=[
                "json/api.json",
                "json/api_url.json",
                ],
            # 错误码配置文件
            error_config_file="json/errno.config",
            # 错误码输出目录
            error_out_dir=os.path.join(dst_dir, "app", "errno"),
            # 错误码范围
            errno_begin=10000,
            errno_end=20000,
            # 生成的项目语言, 支持[go]
            code_type='go',
            # 项目生成路径
            project_dir=dst_dir,
            # project_start_dir=dst_dir,
            # go mod name
            go_module='example',
            # service_name="example",
            # 代码格式模板目录
            mako_dir=os.path.join(os.environ['HOME'], 'gencode', 'mako'),
            # 项目主目录路径
            main_dir=os.path.join(dst_dir, "cmd"),
            # error_package="example/app/errno",
            # graphql
            # graphql_define_package="graphql_define",
            # 请求，应答，数据类型定义生成目录
            graphql_define_dir=os.path.join(dst_dir, "app", "graphql_api", "graphql_define"),
            # 业务接口生成目录
            graphql_api_dir=os.path.join(dst_dir, "app", "graphql_api"),
            # resolver 生成目录
            graphql_resolver_dir=os.path.join(dst_dir, "app", "graphql_api", "graphql_resolver"),
            # resolver type name
            graphql_resolver_type="GraphqlResolver",

            # restful
            # 业务接口生成目录
            restful_api_dir=os.path.join(dst_dir, "app", "restful_api"),
            # 请求，应答，数据类型定义生成目录
            restful_define_dir=os.path.join(dst_dir, 'app', 'restful_api', "restful_define"),
            # restful_define_package="restful_define",
            # restful_api_package="restful_api",

            # grpc
            # proto 生成路径
            grpc_proto_dir=os.path.join(dst_dir, "grpc_pb"),
            # 一些对内的接口目录
            private_grpc_proto_dir=os.path.join(dst_dir, "private_grpc_pb"),
            # 业务接口生成目录
            grpc_api_dir=os.path.join(dst_dir, "app", "grpc_api"),
            # proto中定义的grpc service
            grpc_service_name="GrpcExampleServer",
            # 实例化的grpc接口对应的类名
            grpc_service_type="Server",
            # proto_package="protopb",
            # grpc_package="grpc_pb",

            # grpc_define_pkg_name="define",
            gen_server=True,
            gen_client=None,
            gen_test=True,
            gen_doc=True,
            gen_out=False,
            )
