#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gencode_pkg.go.restful import gen
import os
from gencode_pkg.common import util
from gencode_pkg.common.data_type import InterfaceEnum

if __name__ == '__main__':
    # env = os.environ
    gosrc = os.environ['GOPATH'] + "/src/go_example"  # env['GOPATH'] + "/src/"
    gen.gen_code(
            filenames=["json/newVersion.json", "json/newVersion2.json", "json/login.json"],
            mako_dir="mako/go/restful",
            data_type_out_dir=gosrc + "/app/define",
            func_out_dir=gosrc + "/app/service",
            resolver_out_dir=gosrc + "/app/restful",
            schema_out_dir=gosrc + "/cmd",
            go_test_out_dir=gosrc + "/app/test/restful",
            pro_path=gosrc,
            ip="",
            port=49002,
            gen_server=True,
            gen_client=None,
            )

    util.gen_main([InterfaceEnum.restful], gosrc + "/cmd")
