#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gencode_pkg.go.graphql import gen
import os

if __name__ == '__main__':
    # env = os.environ
    gosrc = os.environ['GOPATH'] + "/src/go_example"  # env['GOPATH'] + "/src/"
    gen.gen_code(
            filenames=["json/newVersion.json", "json/newVersion2.json"],
            mako_dir="mako/go/graphql",
            data_type_out_dir=gosrc + "/app/define",
            resolver_out_dir=gosrc + "/app/resolver",
            schema_out_dir=gosrc + "/main",
            go_test_out_dir=gosrc + "/app/test",
            pro_path=gosrc,
            ip="",
            port=49001,
            gen_server=True,
            gen_client=None,
            query_list=['createJob', 'getAllPermission', 'queryResourcePermission', 'judgePermission', 'login'],
            )
