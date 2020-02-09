#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.common import tool
import os


# 接口文档
class Doc:
    def __init__(self, mako_file, doc_name, doc_dir, apis, enums, errnos):
        self.__apis = apis
        self.__doc_name = doc_name
        self.__doc_dir = doc_dir
        self.__mako_file = mako_file
        self.__enums = enums
        self.__errnos = errnos

    def __gen_tag_doc(self, apis):
        doc_name = os.path.join(self.__doc_dir, self.__doc_name)
        tool.gen_code_file(self.__mako_file,
                           doc_name,
                           apis=apis,
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
