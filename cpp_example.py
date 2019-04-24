#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gen_code
import glob
import os


if __name__ == '__main__':
    env = os.environ
    pro = env['PRONAME'] + "/"
    api_dir = pro + "interface"
    gen_code.gen_code(
            api_dir=api_dir,
            filenames=[x for x in glob.glob(api_dir + "/*.json") if x not in glob.glob(api_dir + "/*_test.json")],
            mako_dir="cpp/beast/mako",
            defines_out_dir=pro + "include/interface",
            server_out_dir=pro + "src/interface",
            client_out_file=pro + "src/client/http_client_interface.h",
            server=True,
            client=True,
            code_type='cpp',
            enums=[],
                     )
