#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gen_code
import glob
import os


if __name__ == '__main__':
    env = os.environ
    config_dir = "cmd"
    gen_code.gen_code(
            config_dir=config_dir,
            filenames=[x for x in glob.glob(config_dir + "/*.json") if x not in glob.glob(config_dir + "/*_test.json")],
            mako_dir="go/graphql/mako",
            defines_out_dir="example/define",
            resolver_out_dir="example/server",
            schema_out_dir="example/mako",
            go_test_dir="example/test",
            server=True,
            client=None,
            code_type='go',
            package='git.ucloudadmin.com/securityhouse/dataflow/dataviewer',
            query_list=['getAllPermission', 'queryResourcePermission', 'judgePermission', 'login'],
            )
