#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# import shutil
from src.common import parser
# import util.python.util as util
from src.common import tool
from src.common import meta
from src.common import code_type
# from src.common import field_type
# from src.go.grpc import gen as go_grpc_gen
# from src.go.restful import gen as go_restful_gen
# from src.common import errno
from src.go.generator import GoGenerator
# import markdown
# import codecs
# from gencode import cpp


def get_parser(filename):
    ext = os.path.splitext(filename)
    if len(ext) == 0:
        print(filename, ext)
        assert False
    ext = ext[-1]
    if ext in ['.json', '.json5']:
        ret = parser.Json5
    elif ext in ['toml']:
        ret = parser.Toml
    else:
        print("不支持的文件类型[%s]", filename)
        assert False
    return ret


def gen_code_files(filenames,
                   **kwargs):
    '''
    mako_dir, errno_out_file,
    service_dir, gen_server, gen_client, gen_test, gen_doc, gen_mock,
    **kwargs):
    '''
    __code_type = kwargs['code_type']
    tool.assert_code_type(__code_type)
    protocols = []
    for filename in filenames:
        parse = get_parser(filename)
        protocol = meta.Protocol(parse(filename).parser())
        protocols.append(protocol)
        # protocol.gen_code_file(  # mako_dir, errno_out_file, service_dir, gen_server, gen_client, gen_test, gen_doc, gen_mock,
        #                       **kwargs)
    if __code_type == code_type.go:
        generator = GoGenerator(protocols, **kwargs)
        generator.gen_code()
    else:
        print("暂不支持的语言类型[%s]", __code_type)
