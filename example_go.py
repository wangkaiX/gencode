#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from src.go.generator import GoGenerator
from src.common import errno
from src.generator import Generator

if __name__ == '__main__':
    service_dir = os.path.join(os.environ['GOPATH'], "src", "example")
    gin = GoGenerator(
            # gin
            module_type="gin",
            # 接口配置文件路径
            filenames=[
                "json/api_gin.json5",
                "json/api_grpc.json5",
                ],
            module_name='example',
            # 错误码配置文件
            errno_configs=[
                errno.ErrnoConfig("json/errno.config", 1000, 2000)
                ],
            # 项目生成路径
            service_dir=service_dir,
            # 代码格式模板目录
            mako_dir=os.path.join(os.environ['HOME'], 'gencode', 'mako'),

            # 生成服务端代码
            gen_server=True,
            # 生成客户端代码
            gen_client=None,
            # 生成服务端接口测试代码
            gen_test=True,
            # 生成接口文档
            gen_doc=True,
            # 生成mock数据
            gen_mock=False,
            )

    generator = Generator([gin])
    generator.gen()
