#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# import copy
# from mako.template import Template
from util.python import util
from src.common import tool
# from gencode.common import meta
from src.go.base.go_protocol_generator_base import GoProtocolGeneratorBase
# import copy


class GoGrpc(GoProtocolGeneratorBase):
    def __init__(self, protocol, **kwargs):
        GoProtocolGeneratorBase.__init__(self, protocol, **kwargs)
        self.__api_dir = kwargs['grpc_api_dir']
        self.__test_dir = os.path.join(self.__api_dir, 'test_grpc')
        self.__grpc_mako_dir = os.path.join(self.mako_dir, 'go', 'grpc')

        self.__proto_package_name = kwargs['proto_package_name']
        self.__proto_dir = kwargs['proto_dir']
        # self.__grpc_dir = kwargs['grpc_api_dir']
        self.__grpc_module_name = kwargs['grpc_module_name']
        if 'grpc_module_type' not in kwargs.keys():
            self.__grpc_module_type = 'GrpcServer'
        else:
            self.__grpc_module_type = kwargs['grpc_module_type']

        self.__package_api_dir = tool.package_name(self.__api_dir, self.go_src_dir)
        self.__package_proto_dir = tool.package_name(self.__proto_dir, self.go_src_dir)
        self.__package_api_name = os.path.basename(self.__api_dir)

    def gen_code(self):
        self.gen_api()
        self.gen_test()

        self.gen_proto()
        self.gen_makefile()
        self.gen_pb()

        self.gen_module_type()
        self.gen_check_arg()
        self.gen_init()
        GoProtocolGeneratorBase.gen_code(self)

    def gen_api(self):
        mako_file = os.path.join(self.__grpc_mako_dir, 'api.go')
        for api in self.protocol.apis:
            filename = "%s.go" % api.name
            filename = os.path.join(self.__api_dir, filename)
            if not os.path.exists(filename):
                tool.gen_code_file(mako_file,
                                   filename,
                                   api=api,
                                   # package_grpc_api_dir=self.__package_grpc_api_dir,
                                   package_proto_dir=self.__package_proto_dir,
                                   package_name=self.__package_api_name,
                                   package_errno_dir=self.package_errno_dir,
                                   json_output=tool.dict2json(api.resp.value_map),
                                   gen_upper_camel=util.gen_upper_camel,
                                   )

    def gen_pb(self):
        old_path = os.path.abspath('.')
        os.chdir(self.__proto_dir)
        r = os.popen("make")
        r.read()
        # os.system("make")
        os.chdir(old_path)

    def gen_test(self):
        self.init_test(self.__test_dir)
        mako_file = os.path.join(self.__grpc_mako_dir, 'test.go')
        for api in self.protocol.apis:
            filename = "%s_test.go" % util.gen_upper_camel(api.name)
            filename = os.path.join(self.__test_dir, filename)
            tool.gen_code_file(mako_file,
                               filename,
                               api=api,
                               package_proto_dir=self.__package_proto_dir,
                               package_module_dir=self.package_module_dir,
                               grpc_module_name=self.__grpc_module_name,
                               json_input=tool.dict2json(api.req.value_map),
                               gen_upper_camel=util.gen_upper_camel,
                               )

    def gen_proto(self):
        # proto
        mako_file = os.path.join(self.__grpc_mako_dir, 'grpc.proto')
        filename = os.path.join(self.__proto_dir, '%s.proto' % self.__proto_package_name)
        tool.gen_code_file(mako_file,
                           filename,
                           package_name=self.__proto_package_name,
                           apis=self.protocol.apis,
                           grpc_module_name=self.__grpc_module_name,
                           gen_upper_camel=util.gen_upper_camel,
                           nodes=self.protocol.nodes,
                           enums=self.protocol.enums,
                           )

    def gen_makefile(self):
        mako_file = os.path.join(self.__grpc_mako_dir, 'proto.mak')
        filename = os.path.join(self.__proto_dir, 'makefile')
        # makefile
        tool.gen_code_file(mako_file,
                           filename,
                           proto_package_name=self.__proto_package_name,
                           )

    def gen_module_type(self):
        mako_file = os.path.join(self.__grpc_mako_dir, 'module_type.go')
        filename = os.path.join(self.__api_dir, "%s.go" % self.__grpc_module_type)
        tool.gen_code_file(mako_file,
                           filename,
                           package_name=self.__package_api_name,
                           grpc_module_type=self.__grpc_module_type,
                           )

    def gen_check_arg(self):
        mako_file = os.path.join(self.__grpc_mako_dir, 'check_arg.go')
        filename = os.path.join(self.__api_dir, 'check_arg.go')
        tool.gen_code_file(mako_file,
                           filename,
                           package_name=self.__package_api_name,
                           grpc_module_type=self.__grpc_module_type,
                           package_proto_dir=self.__package_proto_dir,
                           gen_upper_camel=util.gen_upper_camel,
                           apis=self.protocol.apis,
                           )

    def gen_init(self):
        mako_file = os.path.join(self.__grpc_mako_dir, 'init_grpc.go')
        filename = os.path.join(self.module_dir, 'cmd', 'init_grpc.go')
        # if not os.path.exists(output_file):
        tool.gen_code_file(mako_file,
                           filename,
                           package_api_dir=self.__package_api_dir,
                           package_proto_dir=self.__package_proto_dir,
                           package_module_dir=self.package_module_dir,
                           grpc_module_name=self.__grpc_module_name,
                           )
