#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gencode
import glob


if __name__ == '__main__':
    config_dir = "example"
    gencode.gen_code(config_dir=config_dir,
                     filenames=[x for x in glob.glob(config_dir + "/*.json") if x not in glob.glob(config_dir + "/*_test.json")],
                     mako_dir="./mako",
                     defines_out_dir="./include/interface",
                     server_out_dir="./src/interface",
                     client_out_file="./src/client/http_client_interface.h",
                     server=True,
                     client=True,
                     )
