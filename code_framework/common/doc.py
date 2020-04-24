#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from code_framework.common import tool


# 接口文档
class Doc:
    def __init__(self, mako_file, out_file, apis, enums, errnos):
        self.__apis = apis
        self.__doc_out_file = out_file
        self.__mako_file = mako_file
        self.__enums = enums
        self.__errnos = errnos

    def gen(self):
        tool.gen_code_file(self.__mako_file,
                           self.__doc_out_file,
                           apis=self.__apis,
                           dict2json=tool.dict2json,
                           url_param2text=tool.url_param2text,
                           markdown_full_path=tool.markdown_full_path,
                           enums=self.__enums,
                           is_enum=tool.is_enum,
                           errnos=self.__errnos,
                           nodes2fields=tool.nodes2fields,
                           markdown_type=tool.markdown_type,
                           markdown_note=tool.markdown_note,
                           )
