#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from code_framework.cpp.manager import Manager as CppM
from code_framework.common import type_set


def get_manager(code_type,
                project_name,
                mako_dir,
                log,
                service_dir,
                # doc_outdir,
                ):
    if type_set.cpp == code_type:
        MT = CppM
    else:
        print("未知的编译语言类型[%s], 目前支持的语言类型[%s]" % (code_type, type_set.code_types.keys()))
        assert False
    return MT(project_name=project_name,
              mako_dir=mako_dir,
              log=log,
              service_dir=service_dir,
              # error_code=error_code,
              # error_outdir=error_outdir,
              # doc_outdir=doc_outdir,
              )
