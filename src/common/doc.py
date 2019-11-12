#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.common import tool


class Doc:
    def __init__(self, mako_file, doc_name, doc_dir, apis):
        self.__apis = apis
        self.__doc_name = doc_name
        self.__doc_dir = doc_dir
        self.__tag_doc = {}
        self.__mako_file = mako_file

    def gen_doc(self):
        self.__doc_tag[''] = self.__apis
        for api in self.__.apis:
            self.__tag_doc.setdefault('_' + api.doc_tag, []).append(api)
        for k, v in self.__tag_doc.items():
            self.__gen_tag_doc(k, v)

    def __gen_tag_doc(self, tag, apis):
        filename = "%s%s" % (self.__doc_name, tag)
        md_file = filename + ".md"
        tool.gen_code_file(self.__mako_file,
                           md_file,
                           apis=apis,
                           dict2json=tool.dict2json
                           )
