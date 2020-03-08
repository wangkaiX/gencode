#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.common import tool


# 接口文档
class Doc:
    def __init__(self, mako_file, doc_name, apis, enums, errnos):
        self.__apis = apis
        self.__doc_name = doc_name
        self.__mako_file = mako_file
        self.__enums = enums
        self.__errnos = errnos

    def gen_doc(self, apis):
        tool.gen_code_file(self.__mako_file,
                           self.__doc_name,
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
