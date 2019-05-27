#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# from gencode_pkg.common.data_type import gen_title_name
from mako.template import Template
from gencode_pkg.common import util, data_type
from gencode_pkg.common.util import gen_defines, gen_func, gen_enums
from gencode_pkg.common.read_config import gen_request_response
# import json
import shutil


# def gen_define(st, mako_dir, data_type_out_dir):
#     package = os.path.basename(data_type_out_dir)
#     ctx = {
#             "st": st,
#             "gen_title_name": util.gen_title_name,
#             "to_underline": util.to_underline,
#             "package": package,
#           }
#     mako_file = mako_dir + "/define.mako"
#     util.check_file(mako_file)
#     t = Template(filename=mako_file, input_encoding='utf8')
#     # include_dir = defines_out_dir
#     if not os.path.exists(data_type_out_dir):
#         os.makedirs(data_type_out_dir)

#     data_type_file = "%s/%s.go" % (data_type_out_dir, st.get_name())
#     hfile = open(data_type_file, "w")
#     hfile.write(t.render(**ctx))
#     hfile.close()


# def gen_defines(all_type, mako_dir, data_type_out_dir):
#     for st in all_type:
#         if len(st.fields()) != 0 or len(st.get_nodes()) != 0:
#             gen_define(st, mako_dir, data_type_out_dir)


def gen_servers(all_interface, all_type, common_mako_dir, mako_dir, func_out_dir, resolver_out_dir, query_list, pro_path):
    if not os.path.exists(resolver_out_dir):
        os.makedirs(resolver_out_dir)
    if not os.path.exists(func_out_dir):
        os.makedirs(func_out_dir)
    shutil.copy(mako_dir + "/resolver.go", resolver_out_dir + "/resolver.go")
    for interface in all_interface:
        gen_func(interface, mako_dir, resolver_out_dir, query_list, data_type.InterfaceEnum.graphql, query_list)
        gen_func(interface, common_mako_dir, func_out_dir, query_list, data_type.InterfaceEnum.func, query_list)
    for struct_info in all_type:
        if struct_info.is_resp():
            gen_resolver(struct_info, mako_dir, resolver_out_dir, pro_path)


# def gen_func(interface, mako_dir, func_out_dir, resolver_out_dir, query_list, pro_path, interface_type):
#     resolver = ""
#     mako_file = "func.mako"
#     out_dir = func_out_dir
#     if interface_type == data_type.InterfaceEnum.resolver:
#         mako_file = "func_resolver.mako"
#         out_dir = resolver_out_dir
#         if interface.get_name() in query_list:
#             resolver = "_query"
#         else:
#             resolver = "_mutation"
#     filename = interface.get_name() + resolver

#     filepath = "%s/%s.go" % (out_dir, filename)
#     if os.path.exists(filepath) and interface_type == data_type.InterfaceEnum.func:
#         return

#     mako_file = mako_dir + "/" + mako_file
#     util.check_file(mako_file)

#     t = Template(filename=mako_file, input_encoding="utf8")
#     sfile = open(filepath, "w")
#     sfile.write(t.render(
#         pro_path=pro_path,
#         gen_title_name=util.gen_title_name,
#         interface=interface,
#         ))
#     sfile.close()


def gen_resolver(struct_info, mako_dir, resolver_out_dir, pro_path):
    if not os.path.exists(resolver_out_dir):
        os.makedirs(resolver_out_dir)
    mako_file = mako_dir + "/resolver.mako"
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding="utf8")
    filename = struct_info.get_name() + ".go"
    sfile = open(resolver_out_dir + "/" + filename, "w")
    sfile.write(t.render(
        resp=struct_info,
        gen_title_name=util.gen_title_name,
        pro_path=pro_path,
        ))
    sfile.close()


def gen_schema(all_interface, all_type, all_enum, schema_out_dir, mako_dir, query_list):
    mako_file = mako_dir + "/schema.mako"
    util.check_file(mako_file)
    if not os.path.exists(schema_out_dir):
        os.makedirs(schema_out_dir)

    t = Template(filename=mako_file, input_encoding="utf8")

    ctx = {
            "all_interface": all_interface,
            "all_type": all_type,
            "gen_title_name": util.gen_title_name,
            "query_list": query_list,
            "all_enum": all_enum,
            }

    schema_str = t.render(
            **ctx,
            )
    # schema
    sfile = open(schema_out_dir + '/schema_graphql', "w")
    sfile.write(schema_str)
    sfile.close()

    # schema_go
    sfile = open(schema_out_dir + '/schema.go', "w")
    mako_file = mako_dir + "/schema_go.mako"
    t = Template(filename=mako_file, input_encoding="utf8")
    ctx = {
            "schema": schema_str,
            }
    sfile.write(t.render(
        **ctx,
        ))
    sfile.close()


def gen_tests(all_interface, mako_dir, go_test_out_dir, query_list, pro_path, port):
    # import pdb; pdb.set_trace()
    for interface in all_interface:
        gen_test(interface, mako_dir, go_test_out_dir, query_list, pro_path, port)


# def get_field(fields, resps):
#     fieldstr = ""
#     for field in fields:
#         # import pdb; pdb.set_trace()
#         if field.is_object():
#             fieldstr = fieldstr + field.get_name() + "{\n" + get_field(resps[field.get_type().get_name()].fields(), resps) + "\n}\n"
#         else:
#             fieldstr = fieldstr + '\t' * 3 + field.get_name() + "\n"
#     return fieldstr


# def get_value(field):
#     if field.get_type()._type in ["int", "float", "double", "bool"]:
#         return str(field.get_value())
#     return '"' + str(field.get_value()) + '"'


def remove_quotes(json_str, remove_value=False):
    json_str = str(json_str)
    lines = ""
    for line in json_str.splitlines(True):
        index = line.find(":")
        if -1 == index:
            pass
        elif line.find("{") != -1:
            line = line.replace('"', '', 2)
            if remove_value:
                line = line.replace(':', '', -1)
        else:
            line = line.replace('"', '', 2)
            key = line.split(":")[0]
            # key = key.strip()
            if remove_value:
                line = key+"\n"
            if key.find(data_type.FlagEnum) != -1:
                line = line.replace('"', '', -1)
                # line = line.replace(''', '', -1)
                line = line.replace(data_type.FlagEnum, '', -1)
        lines = lines + line
    return lines[1:-1]


def gen_input_args(req_json):
    # 去除key的 "
    return remove_quotes(req_json)


def gen_out_field(resp_json):
    return remove_quotes(resp_json, True)


def gen_test(interface, mako_dir, go_test_out_dir, query_list, pro_path, port):
    if not os.path.exists(go_test_out_dir):
        os.makedirs(go_test_out_dir)

    if interface.get_name() in query_list:
        query_type = 'query'
    else:
        query_type = 'mutation'
    st = interface.get_req()
    mako_file = mako_dir + "/test.mako"
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding="utf8")
    resp_json = interface.get_resp().to_json_without_i([], False, True)
    output_args = gen_out_field(resp_json)
    null_count = st.get_null_count()
    for i in (list(range(0, null_count)) + [[], list(range(0, null_count))]):
        if type(i) == list:
            find = i
            if i == []:
                name = "none"
            else:
                name = "all"
        else:
            name = str(i)
            find = [i]

        filepath = "%s/%s_%s_test.go" % (go_test_out_dir, interface.get_name(), name)
        sfile = open(filepath, "w")
        req_json = st.to_json_without_i(find, True)
        input_args = gen_input_args(req_json)
        # print(input_args)
        # print(output_args)

        sfile.write(t.render(
            interface=interface,
            query_type=query_type,
            gen_title_name=util.gen_title_name,
            # get_field=get_field,
            name=name,
            input_args=input_args,
            output_args=output_args,
            pro_path=pro_path,
            port=port,
            ))
        sfile.close()


# def gen_enums(all_enum, mako_dir, data_type_out_dir):
#     util.check_file(mako_dir)
#     if not os.path.exists(data_type_out_dir):
#         os.makedirs(data_type_out_dir)

#     filepath = data_type_out_dir + "/" + "enums_gen.go"
#     mako_file = mako_dir + "/enum.mako"
#     t = Template(filename=mako_file, input_encoding="utf8")
#     sfile = open(filepath, "w")
#     sfile.write(t.render(
#         all_enum=all_enum,
#         ))

#     sfile.close()


def gen_run(mako_dir, schema_out_dir, pro_path, ip, port):
    util.check_file(mako_dir)
    if not os.path.exists(schema_out_dir):
        os.makedirs(schema_out_dir)

    filepath = schema_out_dir + "/" + "graphql_run.go"
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
        query_list,
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
    gen_defines(all_type, pro_path, mako_dir, "define.mako", data_type_out_dir + "/graphql_define")
    gen_defines(all_type, pro_path, common_mako_dir, "define.mako", data_type_out_dir)
    gen_enums(all_enum, mako_dir, data_type_out_dir)
    if gen_server:
        # 生成服务端接口实现文件
        gen_run(mako_dir, schema_out_dir, pro_path, ip, port)
        gen_servers(all_interface, all_type, common_mako_dir, mako_dir, func_out_dir, resolver_out_dir, query_list, pro_path)
        gen_schema(all_interface, all_type, all_enum, schema_out_dir, mako_dir, query_list)
        gen_tests(all_interface, mako_dir, go_test_out_dir, query_list, pro_path, port)
