#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from src.go import errno
# from src.common import tool
# from src.common import doc
from src.base.attr_base import AttrBase
# from src.go.gin.gin import GoGin
# from src.common import code_type
# from src.common import errno
# from util.python import util


class GeneratorBase(AttrBase):
    def __init__(self, protocols, **kwargs):  # protocol, mako_dir, errno_out_dir, service_dir, go_src_dir, gen_doc):
        AttrBase.__init__(self, **kwargs)
        self.__protocols = protocols

    @property
    def protocols(self):
        return self.__protocols

    def gen_code(self):
        assert False

    def gen_main(self):
        assert False

    def gen_config(self):
        assert False

    def gen_errno(self):
        assert False
