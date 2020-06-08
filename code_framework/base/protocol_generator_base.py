#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# from src.go import errno
# from src.common import tool
from src.common import doc
from src.base.attr_base import AttrBase
# from util.python import util


# 解析单个配置文件并生成相应代码，文档
class ProtocolGeneratorBase(AttrBase):
    def __init__(self, protocol, **kwargs):  # protocol, mako_dir, errno_out_dir, module_dir, go_src_dir, gen_doc):
        AttrBase.__init__(self, **kwargs)
        self.__protocol = protocol

    @property
    def protocol(self):
        return self.__protocol

    def gen_code(self):
        # self.gen_init()
        self.gen_doc()

    def gen_init(self):
        assert False

    def gen_doc(self):
        mako_file = os.path.join(self.mako_dir, 'doc.md')
        doc_dir = os.path.join(self.module_dir, 'doc')
        # enum_names = [e.name for e in self.protocol.enums]
        # print(mako_file, self.module_name, doc_dir, self.protocol.apis, enum_names)
        # for enum in self.protocol.enums:
        #     print("enum:", enum)
        # assert False
        d = doc.Doc(mako_file=mako_file, doc_name=self.module_name,
                    doc_dir=doc_dir, apis=self.protocol.apis, enums=self.protocol.enums, errnos=self.errnos)
        d.gen_doc()
