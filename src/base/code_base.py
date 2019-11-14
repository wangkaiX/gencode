#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# from src.go import errno
# from src.common import tool
from src.common import doc
from src.base.attr_base import AttrBase
# from util.python import util


class CodeBase(AttrBase):
    def __init__(self, protocol, **kwargs):  # protocol, mako_dir, errno_out_dir, service_dir, go_src_dir, gen_doc):
        AttrBase.__init__(self, **kwargs)
        self.__protocol = protocol

    @property
    def protocol(self):
        return self.__protocol

    def gen_code(self):
        # self.gen_errno()
        self.gen_init()
        # self.gen_main()
        self.gen_doc()

    # def gen_errno(self):
    #     assert False

    # def gen_config(self):
    #     assert False

    def gen_init(self):
        assert False

    def gen_doc(self):
        mako_file = os.path.join(self.mako_dir, 'doc.md')
        doc_dir = os.path.join(self.service_dir, 'doc')
        enum_names = [e.name for e in self.protocol.enums]
        print(mako_file, self.service_name, doc_dir, self.protocol.apis, enum_names)
        d = doc.Doc(mako_file, self.service_name, doc_dir, self.protocol.apis, enum_names)
        d.gen_doc()
