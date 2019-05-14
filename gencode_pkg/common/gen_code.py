#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
import gen_cpp
import gen_go_graphql
import util


def gen_code(
        filenames, mako_dir, defines_out_dir,
        code_type,
        api_dir,
        enums,
        server_out_dir=None,
        schema_out_dir=None,
        resolver_out_dir=None,
        go_test_dir=None,
        package=None,
        client_out_file=None, server=None, client=None, query_list=[]):
    api_dir = util.abs_path(api_dir)
    defines_out_dir = util.abs_path(defines_out_dir)
    mako_dir = util.abs_path(mako_dir)
    if 'cpp' == code_type:
        # assert client_out_file
        assert server_out_dir
        server_out_dir = util.abs_path(server_out_dir)
        gen_cpp.gen_code(
                api_dir=api_dir,
                filenames=filenames,
                mako_dir=mako_dir,
                defines_out_dir=defines_out_dir,
                server_out_dir=server_out_dir,
                client_out_file=client_out_file,
                server=server,
                client=client,
                enums=enums,
                )
    elif 'go' == code_type:
        assert schema_out_dir
        assert resolver_out_dir
        assert go_test_dir
        resolver_out_dir = util.abs_path(resolver_out_dir)
        schema_out_dir = util.abs_path(schema_out_dir)
        go_test_dir = util.abs_path(go_test_dir)
        gen_go_graphql.gen_code(
                filenames=filenames,
                mako_dir=mako_dir,
                defines_out_dir=defines_out_dir,
                resolver_out_dir=resolver_out_dir,
                schema_out_dir=schema_out_dir,
                server=server,
                client=client,
                query_list=query_list,
                go_test_dir=go_test_dir,
                package=package,
                enums=enums,
                api_dir=api_dir,
                )
                '''