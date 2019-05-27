#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gencode_pkg.go.graphql import gen as graphql_gen
from gencode_pkg.go.restful import gen as restful_gen
from gencode_pkg.common import util
from gencode_pkg.common.data_type import InterfaceEnum
import os

if __name__ == '__main__':
    # env = os.environ
    gosrc = os.environ['GOPATH'] + "/src/go_example"  # env['GOPATH'] + "/src/"
    graphql_gen.gen_code(
            filenames=["json/newVersion.json", "json/newVersion2.json", "json/login.json"],
            # filenames=["json/login.json"],
            common_mako_dir="mako/go",
            mako_dir="mako/go/graphql",
            data_type_out_dir=gosrc + "/app/define",
            func_out_dir=gosrc + "/app/service",
            resolver_out_dir=gosrc + "/app/graphqlresolver",
            schema_out_dir=gosrc + "/cmd",
            go_test_out_dir=gosrc + "/app/test/graphql",
            pro_path=gosrc,
            ip="",
            port=49001,
            gen_server=True,
            gen_client=None,
            query_list=['createJob', 'getAllPermission', 'queryResourcePermission', 'judgePermission', 'login'],
            )

    # util.gen_main([InterfaceEnum.graphql, InterfaceEnum.restful], gosrc + "/cmd")

    # env = os.environ
    gosrc = os.environ['GOPATH'] + "/src/go_example"  # env['GOPATH'] + "/src/"
    restful_gen.gen_code(
            filenames=[
                "json/newVersion.json",
                "json/newVersion2.json",
                "json/login.json"
                ],
            common_mako_dir="mako/go",
            mako_dir="mako/go/restful",
            data_type_out_dir=gosrc + "/app/define",
            func_out_dir=gosrc + "/app/service",
            resolver_out_dir=gosrc + "/app/restfulresolver",
            schema_out_dir=gosrc + "/cmd",
            go_test_out_dir=gosrc + "/app/test/restful",
            pro_path=gosrc,
            ip="",
            port=49002,
            gen_server=True,
            gen_client=None,
            )

    util.gen_main([InterfaceEnum.restful, InterfaceEnum.graphql], gosrc + "/cmd")
