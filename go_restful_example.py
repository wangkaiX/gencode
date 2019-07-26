#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gencode.go.restful import gen
import os
from gencode.common import util
from gencode.common.data_type import InterfaceEnum

if __name__ == '__main__':
    # env = os.environ
    gopath = os.environ['GOPATH']
    assert gopath
    gosrc = os.environ['GOPATH'] + "/src/go_example"  # env['GOPATH'] + "/src/"
    gen.gen_code(
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

    util.gen_main([InterfaceEnum.restful], gosrc + "/cmd")
