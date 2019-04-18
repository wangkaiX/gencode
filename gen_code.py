#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gen_cpp
import gen_go_graphql
import util


def gen_code(
        config_dir, filenames, mako_dir, defines_out_dir, server_out_dir,
        code_type,
        schema_out_path=None,
        client_out_file=None, server=None, client=None, query_list=[]):
    config_dir = util.abs_path(config_dir)
    mako_dir = util.abs_path(mako_dir)
    defines_out_dir = util.abs_path(defines_out_dir)
    server_out_dir = util.abs_path(server_out_dir)
    if 'cpp' == code_type:
        # assert client_out_file
        gen_cpp.gen_code(
                config_dir=config_dir,
                filenames=filenames,
                mako_dir=mako_dir,
                defines_out_dir=defines_out_dir,
                server_out_dir=server_out_dir,
                client_out_file=client_out_file,
                server=server,
                client=client,
                )
    elif 'go' == code_type:
        assert schema_out_path
        gen_go_graphql.gen_code(
                config_dir=config_dir,
                filenames=filenames,
                mako_dir=mako_dir,
                defines_out_dir=defines_out_dir,
                server_out_dir=server_out_dir,
                schema_out_path=schema_out_path,
                server=server,
                client=client,
                query_list=query_list,
                )
