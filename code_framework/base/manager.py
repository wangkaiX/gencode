#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from code_framework.common import tool
# from code_framework.common import type_set
# from code_framework.cpp.manager import Manager as cppM


class Manager:
    def __init__(self,
                 project_name,
                 code_type,
                 # 代码格式模板目录
                 mako_dir,
                 # 项目生成路径
                 service_dir,
                 # 错误码配置文件
                 error_code,
                 # 错误码输出目录
                 error_outdir,
                 doc_outdir,
                 ):
        self._project_name = project_name
        self._code_type = code_type
        self._mako_dir = mako_dir
        self._service_dir = service_dir
        self._error_code = error_code
        self._error_outdir = error_outdir
        self._doc_outdir = doc_outdir
        self._frameworks = []

    def add(self, framework):
        tool.assert_framework_type(self._code_type, framework.framework)
        self._frameworks.append(framework)

    #  def gen(self):
    #      for framework in self._frameworks:
    #          if type_set.cpp == self._code_type:
    #              self._gen_cpp(framework)

    #  def _gen_cpp(self, framework):
    #      manager = cppM(mako_dir=self._mako_dir, service_dir=self._service_dir, framework=framework)
    #      manager.gen()
