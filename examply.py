#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from gencode.common import gen

if __name__ == '__main__':
    go_path = os.environ['GOPATH']
    go_src = os.path.join(go_path, "src")
    dst_dir = os.environ['GOPATH'] + "/src/example"  # env['GOPATH'] + "/src/"
    dst_dir2 = os.environ['GOPATH'] + "/src/abc2"  # env['GOPATH'] + "/src/"
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
            go_src=go_src,
            # 代码格式模板目录
            mako_dir=os.path.join(os.environ['HOME'], 'gencode', 'mako'),
            # 项目主目录路径
            main_dir=os.path.join(dst_dir, "cmd"),
            # graphql
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

            # grpc
            # proto 生成路径
            grpc_proto_dir=os.path.join(dst_dir, "grpc_pb"),
            # 一些对内的接口目录
            # private_grpc_proto_dir=os.path.join(dst_dir, "private_grpc_pb"),
            # 业务接口生成目录
            grpc_api_dir=os.path.join(dst_dir, "app", "grpc_api"),
            # proto中定义的grpc service
            grpc_service_name="GrpcExampleServer",
            # 实例化的grpc接口对应的类名
            grpc_service_type="Server",
            # proto文件中的包名
            proto_package="protopb",
            # grpc_package="grpc_pb",

            gen_server=True,
            gen_client=None,
            gen_test=True,
            gen_doc=True,
            gen_out=False,
            )
