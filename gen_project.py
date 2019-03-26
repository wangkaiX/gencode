#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gencode
import glob
import os


if __name__ == '__main__':
    env = os.environ
    pro = env['PRONAME'] + "/"
    config_dir = pro + "interface"
    gencode.gen_code(config_dir=config_dir,
                     filenames=[x for x in glob.glob(config_dir + "/*.json") if x not in glob.glob(config_dir + "/*_test.json")],
                     mako_dir="./mako",
                     defines_out_dir=pro + "include/interface",
                     server_out_dir=pro + "src/interface",
                     client_out_file=pro + "src/client/http_client_interface.h",
                     server=True,
                     client=True,
                     )
