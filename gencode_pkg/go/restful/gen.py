#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# from gencode_pkg.common.data_type import gen_title_name
from mako.template import Template
from gencode_pkg.common import util, data_type
from gencode_pkg.common.util import gen_defines, gen_func, gen_enums
from gencode_pkg.common.read_config import gen_request_response
# import json
# import shutil


def gen_servers(all_interface, all_type, common_mako_dir, mako_dir, func_out_dir, resolver_out_dir, pro_path):
    if not os.path.exists(resolver_out_dir):
        os.makedirs(resolver_out_dir)
    if not os.path.exists(func_out_dir):
        os.makedirs(func_out_dir)
    # shutil.copy(mako_dir + "/resolver.go", resolver_out_dir + "/resolver.go")
    gen_resolver(all_interface, mako_dir, resolver_out_dir, pro_path)
    for interface in all_interface:
        gen_func(interface, common_mako_dir, func_out_dir, pro_path, data_type.InterfaceEnum.func)
#     for struct_info in all_type:
#         if struct_info.is_resp():
#             gen_resolver(struct_info, mako_dir, resolver_out_dir, pro_path)


def gen_resolver(all_interface, mako_dir, resolver_out_dir, pro_path):
    if not os.path.exists(resolver_out_dir):
        os.makedirs(resolver_out_dir)
    mako_file = mako_dir + "/router.mako"
    util.check_file(mako_file)

    filename = "router.go"
    router_file = resolver_out_dir + "/" + filename
    if os.path.exists(router_file):
        return

    t = Template(filename=mako_file, input_encoding="utf8")
    sfile = open(router_file, "w")
    sfile.write(t.render(
        all_interface=all_interface,
        gen_title_name=util.gen_title_name,
        pro_path=pro_path,
        ))
    sfile.close()


def gen_tests(all_interface, mako_dir, go_test_out_dir, pro_path, port):
    for interface in all_interface:
        gen_test(interface, mako_dir, go_test_out_dir, pro_path, port)


def gen_url_param(st):
    # import pdb
    # pdb.set_trace()
    p = ""
    for field in st.fields():
        p += "%s=%s&" % (field.get_name(), field.get_value())
    return p[:-1]


def gen_test(interface, mako_dir, go_test_out_dir, pro_path, port):
    if not os.path.exists(go_test_out_dir):
        os.makedirs(go_test_out_dir)

    st = interface.get_req()
    mako_file = mako_dir + "/test.mako"
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding="utf8")
    # resp_json = interface.get_resp().to_json_without_i([], False, True)
    # output_args = gen_out_field(resp_json)
    null_count = st.get_null_count()
    url_param = gen_url_param(interface.get_url_param())
    for i in (list(range(0, null_count)) + [[], list(range(0, null_count))]):
        if type(i) == list:
            find = i
            if i == []:
                name = "all"
            else:
                name = "none"
        else:
            name = str(i)
            find = [i]

        filepath = "%s/%s_%s_test.go" % (go_test_out_dir, interface.get_name(), name)
        sfile = open(filepath, "w")
        req_json = st.to_json_without_i(find, True, False, True)
        # print(input_args)

        sfile.write(t.render(
            interface=interface,
            gen_title_name=util.gen_title_name,
            # get_field=get_field,
            name=name,
            input_args=req_json,
            # output_args=output_args,
            url_param=url_param,
            pro_path=pro_path,
            port=port,
            ))
        sfile.close()


def gen_run(mako_dir, schema_out_dir, pro_path, ip, port):
    util.check_file(mako_dir)
    if not os.path.exists(schema_out_dir):
        os.makedirs(schema_out_dir)

    filepath = schema_out_dir + "/" + "restful_run.go"
    if os.path.exists(filepath):
        return
    mako_file = mako_dir + "/run.mako"
    t = Template(filename=mako_file, input_encoding="utf8")
    sfile = open(filepath, "w")
    sfile.write(t.render(
        pro_path=pro_path,
        ip=ip,
        port=port,
        ))

    sfile.close()


def gen_code(
        filenames,
        common_mako_dir,
        mako_dir,
        data_type_out_dir,
        func_out_dir,
        resolver_out_dir, schema_out_dir,
        go_test_out_dir,
        pro_path,
        ip,
        port,
        gen_server, gen_client):
    assert filenames
    assert mako_dir
    assert data_type_out_dir
    assert resolver_out_dir
    assert schema_out_dir
    assert go_test_out_dir
    assert pro_path
    if not ip:
        ip = ""
    assert port

    pro_path = util.package_name(pro_path)
    all_interface = []
    all_type = []
    all_enum = []

    common_mako_dir = util.abs_path(common_mako_dir)
    mako_dir = util.abs_path(mako_dir)
    data_type_out_dir = os.path.abspath(data_type_out_dir)
    resolver_out_dir = util.abs_path(resolver_out_dir)
    schema_out_dir = util.abs_path(schema_out_dir)
    go_test_out_dir = util.abs_path(go_test_out_dir)

    # 数据整理
    # print(filenames)
    for filename in filenames:
        interfaces = gen_request_response(filename, all_enum)
        util.add_interface(all_interface, interfaces)
        for interface in interfaces:
            for t in interface.get_types():
                util.add_struct(all_type, t)
            for enum in interface.get_enums():
                util.add_enum(all_enum, enum)

    # 生成.h文件
    gen_defines(all_type, pro_path, common_mako_dir, "define.mako", data_type_out_dir)
    gen_enums(all_enum, mako_dir, data_type_out_dir)
    if gen_server:
        # 生成服务端接口实现文件
        gen_run(mako_dir, schema_out_dir, pro_path, ip, port)
        gen_servers(all_interface, all_type, common_mako_dir, mako_dir, func_out_dir, resolver_out_dir, pro_path)
        gen_tests(all_interface, mako_dir, go_test_out_dir, pro_path, port)
