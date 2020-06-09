#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from code_framework.common import gen
from code_framework.common import errno

if __name__ == '__main__':
    go_path = os.environ['GOPATH']
    go_src = os.path.join(go_path, "src")
    dst_dir = os.environ['GOPATH'] + "/src/example"  # env['GOPATH'] + "/src/"
    # dst_dir2 = os.environ['GOPATH'] + "/src/abc2"  # env['GOPATH'] + "/src/"
    gen.gen_code_files(
            code_type="go",
            module="gin",
            # 接口配置文件路径
            filenames=[
                "json/api_gin.json5",
                "json/api_grpc.json5",
                ],
            name='example',
            # 错误码配置文件
            errno_configs=[
                errno.ErrnoConfig("json/errno.config", 1000, 2000)
                ],
            # 错误码输出目录
            errno_dir=os.path.join(dst_dir, "app", "errno"),
            # 项目生成路径
            service_dir=dst_dir,
            # project_start_dir=dst_dir,
            go_src_dir=go_src,
            # 代码格式模板目录
            mako_dir=os.path.join(os.environ['HOME'], 'gencode', 'mako'),

            # graphql
            # 请求，应答，数据类型定义生成目录
            graphql_define_dir=os.path.join(dst_dir, "app", "graphql_api", "graphql_define"),
            # 业务接口生成目录
            graphql_api_dir=os.path.join(dst_dir, "app", "graphql_api"),
            # resolver 生成目录
            graphql_resolver_dir=os.path.join(dst_dir, "app", "graphql_api", "graphql_resolver"),
            # resolver type name
            graphql_resolver_type="GraphqlResolver",

            # go_gin
            # 业务接口生成目录
            go_gin_api_dir=os.path.join(dst_dir, "app", "gin_api"),
            # 请求，应答，数据类型定义生成目录
            go_gin_define_dir=os.path.join(dst_dir, 'app', 'gin_api', "gin_define"),

            # grpc
            # proto 生成路径
            proto_dir=os.path.join(dst_dir, "grpc_pb"),
            # 业务接口生成目录
            grpc_api_dir=os.path.join(dst_dir, "app", "grpc_api"),
            # proto中定义的grpc service
            grpc_name="GrpcExampleServer",
            # 实例化的grpc接口对应的类名
            grpc_service_type="Server",
            # proto文件中的包名
            proto_package_name="protopb",

            gen_client=None,
            gen_server=True,
            # 当生成服务端的时候，才会生成test
            gen_test=True,
            gen_doc=True,
            gen_mock=False,
            )
