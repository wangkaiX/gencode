#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from code_framework.common import tool
# from code_framework.common import type_set
# from code_framework.cpp.manager import Manager as cppM


class ServiceBase:
    def __init__(self,
                 service_name,
                 # 代码格式模板目录
                 mako_dir,
                 # log
                 service_dir,
                 # 错误码配置文件
                 error_code,
                 ):
        self._service_name = service_name
        self._mako_dir = mako_dir
        self._service_dir = service_dir
        self._error_code = error_code
        self._modules = []

    def add(self, module):
        # tool.assert_type(self._code_type, module.network)
        self._modules.append(module)

    #  def gen(self):
    #      for module in self._modules:
    #          if type_set.cpp == self._code_type:
    #              self._gen_cpp(module)

    #  def _gen_cpp(self, module):
    #      manager = cppM(mako_dir=self._mako_dir, dir=self._dir, module=module)
    #      manager.gen()
