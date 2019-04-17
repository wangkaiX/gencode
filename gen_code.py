#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gen_cpp
import gen_go_graphql


def gen_code(config_dir, filenames, mako_dir, defines_out_dir, server_out_dir, client_out_file, server, client, code_type, query_list):
    if 'cpp' == code_type:
        gen_cpp.gen_code(config_dir=config_dir,
                         filenames=filenames,
                         mako_dir=mako_dir,
                         defines_out_dir=defines_out_dir,
                         server_out_dir=server_out_dir,
                         client_out_file=client_out_file,
                         server=server,
                         client=client,
                         )
    elif 'go' == code_type:
        gen_go_graphql.gen_code(config_dir=config_dir,
                         filenames=filenames,
                         mako_dir=mako_dir,
                         defines_out_dir=defines_out_dir,
                         server_out_dir=server_out_dir,
                         client_out_file=client_out_file,
                         server=server,
                         client=client,
                         query_list=query_list,
                         )
