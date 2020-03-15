#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from code_framework.common import tool
from code_framework.common import field_type
from code_framework.cpp.generator import GeneratorManager as cppGM


class GeneratorManager:
    def __init__(self,
                 project_name,
                 code_type,
                 # 代码格式模板目录
                 mako_dir,
                 # 项目生成路径
                 service_dir,
                 # 错误码配置文件
                 errno_configs,
                 # 错误码输出目录
                 errno_dir):
        self.__project_name = project_name
        self.__code_type = code_type
        self.__mako_dir = mako_dir
        self.__service_dir = service_dir
        self.__errno_configs = errno_configs
        self.__errno_dir = errno_dir
        self.__protocols = []

    def add(self, protocol):
        tool.assert_framework_type(self.__code_type, protocol.framework)
        self.__protocols.append(protocol)

    def gen(self):
        for protocol in self.__protocols:
            if field_type.cpp == self.__code_type:
                self.__gen_cpp(protocol)

    def __gen_cpp(self, protocol):
        gm = cppGM(protocol)
        gm.gen()
