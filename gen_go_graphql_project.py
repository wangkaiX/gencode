#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gen_code
import glob
import os


if __name__ == '__main__':
    env = os.environ
    pro = env['PRONAME'] + "/"
    config_dir = pro + "interface"
    gen_code.gen_code(config_dir=config_dir,
                     filenames=[x for x in glob.glob(config_dir + "/*.json") if x not in glob.glob(config_dir + "/*_test.json")],
                     mako_dir="go/graphql/mako",
                     defines_out_dir="example/define",
                     server_out_dir="example/server",
                     client_out_file="example/mako",
                     # client_out_file=None,
                     server=True,
                     client=None,
                     code_type='go',
                     query_list=['create_crontab_job'],
                     )
