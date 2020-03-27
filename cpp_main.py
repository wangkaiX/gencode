#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from code_framework.common import generator
from code_framework.common import errno
from code_framework.common import meta
from code_framework.common import type_set

if __name__ == '__main__':
    dst_dir = os.path.join("example", "cpp", "src")

    generatorManager = generator.GeneratorManager(
            project_name="project_example",
            code_type="cpp",
            # 代码格式模板目录
            mako_dir=os.path.join(os.environ['HOME'], 'gencode', 'mako'),
            # 项目生成路径
            service_dir=dst_dir,
            errno_configs=[
                # 错误码配置文件
                errno.ErrnoConfig("json/errno.config", 1000, 2000),
                ],
            # 错误码输出目录
            errno_dir=os.path.join(dst_dir, "src", "types", "errno"),
            )

    protocol_websocket = meta.CodeFramework(
            service_name='example',
            framework=type_set.Cpp.beast_websocket_async,
            adapt_type=type_set.CppAdapt.nlohmann_json,
            # 接口配置文件路径
            protocol_filename="json/api_gin.json5",
            heartbeat_interval_second=5,
            heartbeat_loss_max=3,
            gen_client=True,
            gen_server=True,
            gen_test=True,
            gen_doc=True,
            gen_mock=True,
            )

    generatorManager.add(protocol_websocket)
    generatorManager.gen()
