#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.common import tool
import os


class Doc:
    def __init__(self, mako_file, doc_name, doc_dir, apis, enums, errnos):
        self.__apis = apis
        self.__doc_name = doc_name
        self.__doc_dir = doc_dir
        self.__tag_api = {}
        self.__mako_file = mako_file
        self.__enums = enums
        self.__errnos = errnos

    def gen_doc(self):
        self.__tag_api[''] = self.__apis
        for api in self.__apis:
            for doc_tag in api.doc_tags:
                self.__tag_api.setdefault('_' + doc_tag, []).append(api)
        for k, v in self.__tag_api.items():
            self.__gen_tag_doc(k, v)

    def __gen_tag_doc(self, tag, apis):
        filename = "%s%s" % (self.__doc_name, tag)
        markdown_file = os.path.join(self.__doc_dir, filename + ".md")
        # enum_names = [enum.name for enum in self.__enums]
        tool.gen_code_file(self.__mako_file,
                           markdown_file,
                           apis=apis,
                           dict2json=tool.dict2json,
                           url_param2text=tool.url_param2text,
                           markdown_full_path=tool.markdown_full_path,
                           enums=self.__enums,
                           # enum_names=enum_names,
                           is_enum=tool.is_enum,
                           errnos=self.__errnos,
                           nodes2fields=tool.nodes2fields,
                           markdown_type=tool.markdown_type,
                           markdown_note=tool.markdown_note,
                           )
