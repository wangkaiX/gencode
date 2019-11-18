#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.common import tool
from src.common import code_type
from src.go.base.go_generator_base import GeneratorGoBase
from src.go.gin.gin import GoGin
from src.go.grpc.grpc import GoGrpc


class GoGenerator(GeneratorGoBase):
    def __init__(self, protocols, **kwargs):  # protocol, mako_dir, errno_out_dir, service_dir, go_src_dir, gen_doc):
        GeneratorGoBase.__init__(self, protocols, **kwargs)
        go_src_dir = kwargs['go_src_dir']
        self.__package_service_dir = tool.package_name(self.service_dir, go_src_dir)

    def gen_code(self):
        for protocol in self.protocols:
            if code_type.go_gin == protocol.framework_type:
                generator = GoGin(protocol, **self.kwargs)
            elif code_type.grpc == protocol.framework_type:
                generator = GoGrpc(protocol, **self.kwargs)

            else:
                print("go语言暂不支持框架[%s]", protocol.framework_type)
                assert False
            generator.gen_code()
        GeneratorGoBase.gen_code(self)
