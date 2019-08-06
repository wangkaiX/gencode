#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from gencode.common import gen

if __name__ == '__main__':
    gopath = os.environ['GOPATH']
    assert gopath
    gosrc = os.environ['GOPATH'] + "/src/example"  # env['GOPATH'] + "/src/"
    gen.gen_code(
            filenames=[
                "json/newVersion3.json",
                ],
            code_type='go',
            project_name="example",
            mako_dir="~/gencode/mako",
            # graphql_dir=gosrc + "/app/graphql_api",
            # graphql_schema_dir="custom",
            # graphql_define_pkg_name="custom",
            # graphql_resolver_pkg_name="custom",
            # graphql_ip="",
            # graphql_port=49001,
            # restful_dir=gosrc + "app/restful_api",
            # restful_define_pkg_name="custom",
            # restful_resolver_pkg_name="custom",
            # restful_ip="",
            # restful_port=49002,
            grpc_proto_dir=os.path.join(gosrc, "proto"),
            grpc_pb_dir=os.path.join(gosrc, "app", "grpc_api"),
            grpc_define_pkg_name="define",
            grpc_ip="0.0.0.0",
            grpc_port=49003,
            gen_server=True,
            gen_client=None,
            gen_test=None,
            )
