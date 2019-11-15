#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.common import tool
from src.go.base.go_generator_base import GeneratorGoBase


class Generator(GeneratorGoBase):
    def __init__(self, protocols, **kwargs):  # protocol, mako_dir, errno_out_dir, service_dir, go_src_dir, gen_doc):
        GeneratorGoBase.__init__(self, protocols, **kwargs)
        go_src_dir = kwargs['go_src_dir']
        self.__package_service = tool.package_name(self.service_dir, go_src_dir)
