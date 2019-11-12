#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# import shutil
from src.common import parser
# import util.python.util as util
# from src.common import tool
from src.common import meta
# from src.common import field_type
# from src.go.grpc import gen as go_grpc_gen
# from src.go.restful import gen as go_restful_gen
# from src.common import errno
# import markdown
# import codecs
# from gencode import cpp


def gen_server():
    pass


def gen_client():
    pass


def gen_test():
    pass


def get_parser(filename):
    ext = os.path.splitext(filename)
    print(filename, ext)
    if len(ext) > 0 and ext[-1] in ['.json', '.json5']:
        ret = parser.Json5
    else:
        assert False
    return ret


def gen_code_files(filenames, mako_dir, errno_out_file,
                   service_dir, gen_server, gen_client, gen_test, gen_doc, gen_mock,
                   **kwargs):
    protocols = []
    for filename in filenames:
        parse = get_parser(filename)
        protocol = meta.Protocol(parse(filename).parser())
        protocols.append(protocol)
        protocol.gen_code_file(mako_dir, errno_out_file, service_dir, gen_server, gen_client, gen_test, gen_doc, gen_mock,
                               **kwargs)
