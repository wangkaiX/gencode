#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from data_type import gen_title_name
from mako.template import Template
from pkg.common import util
from pkg.common.read_config import gen_request_response
import json
import shutil


all_type = {}
inputs = []
# g_enums = []
g_package = None
# g_api_dir = None


def get_resolver_type(_type):
    if type(_type) == str:
        return _type + "Resolver"
    return _type.get_name() + "Resolver"


def get_list_type(field):
    if field.is_list():
        if field.is_object():
            return "[]*" + field.get_base_type().get_name() + "Resolver"
        else:
            return field.get_type()._go


def get_addr_op(field):
    if field.is_list():
        if field.is_object():
            return "&"
        else:
            return ""
    if field.is_object():
        return "&"
    return ""


def get_resolver_rettype(field):
    if field.get_type()._type == 'time':
        return "graphql.Time"
    if field.is_object():
        if field.is_list():
            return "*[]*" + field.get_base_type().get_name() + "Resolver"
        else:
            return field.get_type()._go + "Resolver"
    else:
        return field.get_type()._go


def gen_define(st, mako_dir, defines_out_dir, is_response=False):
    ctx = {
            "st": st,
            "gen_title_name": util.gen_title_name,
            "is_response": is_response,
            "to_underline": util.to_underline,
            "package": g_package,
          }
    mako_file = mako_dir + "/defines.mako"
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding='utf8')
    include_dir = defines_out_dir
    if not os.path.exists(include_dir):
        os.makedirs(include_dir)

    head_file = "%s/%s.go" % (include_dir, st.get_name())
    hfile = open(head_file, "w")
    hfile.write(t.render(**ctx))
    hfile.close()


def gen_defines(reqs, resps, mako_dir, defines_out_dir):
    for k, v in all_type.items():
        if len(v.fields()) != 0:
            if k in resps.keys():
                is_response = True
            else:
                is_response = False
            gen_define(v, mako_dir, defines_out_dir, is_response)


def gen_servers(req_resp_list, reqs, resps, mako_dir, resolver_out_dir, query_list):
    if not os.path.exists(resolver_out_dir):
        os.makedirs(resolver_out_dir)
    shutil.copy(mako_dir + "/resolver.go", resolver_out_dir + "/resolver.go")
    for interface_name, req, resp in req_resp_list:
        req = util.get_first_value(req)
        resp = util.get_first_value(resp)
        gen_func(interface_name, req, resp, mako_dir, resolver_out_dir, query_list)
    for k, v in resps.items():
        gen_resolver(v, mako_dir, resolver_out_dir)


def gen_func(interface_name, req, resp, mako_dir, resolver_out_dir, query_list):
    if not os.path.exists(resolver_out_dir):
        os.makedirs(resolver_out_dir)

    if interface_name in query_list:
        filename = interface_name + "_query"
    else:
        filename = interface_name + "_mutation"
    filepath = resolver_out_dir + "/" + filename + ".go"
    if os.path.exists(filepath):
        return

    mako_file = mako_dir + "/func.mako"
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding="utf8")

    sfile = open(filepath, "w")
    sfile.write(t.render(
        class_name=gen_title_name(interface_name),
        req=req,
        resp=resp,
        package=g_package,
        ))
    sfile.close()


def gen_resolver(resp, mako_dir, resolver_out_dir):
    if not os.path.exists(resolver_out_dir):
        os.makedirs(resolver_out_dir)
    mako_file = mako_dir + "/resolver.mako"
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding="utf8")
    filename = resp.get_name() + ".go"
    sfile = open(resolver_out_dir + "/" + filename, "w")
    sfile.write(t.render(
        resp=resp,
        gen_title_name=util.gen_title_name,
        get_resolver_type=get_resolver_type,
        get_list_type=get_list_type,
        get_addr_op=get_addr_op,
        get_resolver_rettype=get_resolver_rettype,
        package=g_package,
        ))
    sfile.close()


def gen_schema(schema_out_dir, reqs, resps, req_resp_list, mako_dir, query_list):
    mako_file = mako_dir + "/schema.mako"
    print("filename", schema_out_dir)
    # dirname = os.path.dirname(schema_out_dir)
    if not os.path.exists(schema_out_dir):
        os.makedirs(schema_out_dir)
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding="utf8")
    sfile = open(schema_out_dir + '/schema.go', "w")
    r_p_list = []
    for interface_name, req, resp in req_resp_list:
        req = util.get_first_value(req)
        resp = util.get_first_value(resp)
        r_p_list.append([interface_name, req, resp])

    # reqs = list(reqs.values())
    # resps = list(resps.values())
    # reqs = util.stable_unique(reqs)
    # resps = util.stable_unique(resps)

    ctx = {
            "services": r_p_list,
            "reqs": reqs,
            "resps": resps,
            "gen_title_name": util.gen_title_name,
            "query_list": query_list,
            "all_type": all_type,
            "inputs": inputs,
            "package": g_package,
            "enums": g_enums,
            }
    sfile.write(t.render(
        **ctx,
        ))

    schemafile = open(schema_out_dir + '/schema.graphql', "w")
    schema_mako_file = mako_dir + "/schema_graphql.mako"
    tschema = Template(filename=schema_mako_file, input_encoding="utf8")
    schemafile.write(tschema.render(
        **ctx,
        ))


def gen_tests(req_resp_list, reqs, resps, mako_dir, go_test_dir, query_list, enum_fields):
    # import pdb; pdb.set_trace()
    for interface_name, req, resp in req_resp_list:
        req = util.get_first_value(req)
        resp = util.get_first_value(resp)
        gen_test(interface_name, req, resp, resps, mako_dir, go_test_dir, query_list, enum_fields)


def get_field(fields, resps):
    fieldstr = ""
    for field in fields:
        # import pdb; pdb.set_trace()
        if field.is_object():
            fieldstr = fieldstr + field.get_name() + "{\n" + get_field(resps[field.get_base_type().get_name()].fields(), resps) + "\n}\n"
        else:
            fieldstr = fieldstr + '\t' * 3 + field.get_name() + "\n"
    return fieldstr


def get_value(field):
    if field.get_base_type()._type in ["int", "float", "double", "bool"]:
        return str(field.get_value())
    return '"' + str(field.get_value()) + '"'


def remove_quotes(json_str, enum_fields):
    json_str = str(json_str)
    lines = ""
    for line in json_str.splitlines(True):
        index = line.find(":")
        if -1 == index:
            pass
        else:
            line = line.replace('"', '', 2)
            key = line.split(":")[0]
            key = key.strip()
            if key in enum_fields:
                line = line.replace('"', '', 2)
        lines = lines + line
    print("lines:", lines[1:-1])
    return lines[1:-1]


def get_input_args(interface_name, enum_fields):
    if not os.path.exists(g_api_dir):
        print(g_api_dir, "not exists")
        assert False
    print("api_dir:", g_api_dir)
    jmap = util.readjson("%s/%s_test.json" % (g_api_dir, interface_name))
    # 只保留请求
    del jmap[list(jmap.keys())[1]]
    if not jmap[list(jmap.keys())[0]]:
        return ""
    json_str = json.dumps(jmap, separators=(',', ':'), indent=4, ensure_ascii=False)
    # 去除key的 "
    return remove_quotes(json_str, enum_fields)


def gen_test(interface_name, req, resp, resps, mako_dir, go_test_dir, query_list, enum_fields):
    if not os.path.exists(go_test_dir):
        os.makedirs(go_test_dir)

    if interface_name in query_list:
        query_type = 'query'
    else:
        query_type = 'mutation'
    filepath = go_test_dir + "/" + interface_name + "_test.go"

    mako_file = mako_dir + "/test.mako"
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding="utf8")

    sfile = open(filepath, "w")
    print("test file:", filepath)
    sfile.write(t.render(
        class_name=gen_title_name(interface_name),
        req=req,
        resp=resp,
        resps=resps,
        query_type=query_type,
        gen_title_name=util.gen_title_name,
        interface_name=interface_name,
        get_field=get_field,
        input_args=get_input_args(interface_name, enum_fields),
        package=g_package,
        enum_fields=enum_fields,
        ))
    sfile.close()


def gen_enums(mako_dir, defines_out_dir, enums):
    if not os.path.exists(mako_dir):
        print(mako_dir, "not exists")
        assert False
    if not os.path.exists(defines_out_dir):
        os.makedirs(defines_out_dir)

    filepath = defines_out_dir + "/" + "vars_gen.go"
    mako_file = mako_dir + "/enum.mako"
    t = Template(filename=mako_file, input_encoding="utf8")
    sfile = open(filepath, "w")
    es = []
    for k, vs in enums.items():
        for v in vs:
            es.append(v)
    es = util.stable_unique(es)
    sfile.write(t.render(
        es=es,
        ))

    sfile.close()


def gen_main(mako_dir, schema_out_dir, package):
    if not os.path.exists(mako_dir):
        print(mako_dir, "not exists")
        assert False
    if not os.path.exists(schema_out_dir):
        os.makedirs(schema_out_dir)

    filepath = schema_out_dir + "/" + "main.go"
    if os.path.exists(filepath):
        return
    mako_file = mako_dir + "/main.mako"
    t = Template(filename=mako_file, input_encoding="utf8")
    sfile = open(filepath, "w")
    sfile.write(t.render(
        package=package,
        ))

    sfile.close()


def gen_code(
        filenames, mako_dir,
        data_type_out_dir, resolver_out_dir, schema_out_dir,
        go_test_dir,
        package=None,
        gen_server=None, gen_client=None):
    assert package
    # assert api_dir
    global g_package
    global g_enums
    # global g_api_dir
    # g_api_dir = api_dir
    g_package = package
    req_resp_list = []
    reqs = {}
    resps = {}

    #
    mako_dir = util.abs_path(mako_dir)
    # api_dir = os.path.abspath(api_dir)
    defines_out_dir = util.abs_path(defines_out_dir)
    resolver_out_dir = util.abs_path(resolver_out_dir)

    # 数据整理
    print(filenames)
    for filename in filenames:
        # test_case.gen_test_case(filename)
        basename = os.path.basename(filename)
        interface_name = basename.split(".")[0]
        req, resp = gen_request_response(filename, enums)
        req_resp_list.append([interface_name, req, resp])
        # keys = list(req.keys())
        # if len(keys) != 0:
        #     inputs.append(keys[0])
        for k, v in req.items():
            util.add_struct(reqs, k)
            util.add_struct(all_type, k)
            for field in v.fields():
                reqs[k].add_field(field)
                all_type[k].add_field(field)
            inputs.append(k)

        for k, v in resp.items():
            util.add_struct(resps, k)
            util.add_struct(all_type, k)
            for field in v.fields():
                resps[k].add_field(field)
                all_type[k].add_field(field)
            # resps[k].add_field(err_code)
            # resps[k].add_field(err_msg)
            # all_type[k].add_field(err_code)
            # all_type[k].add_field(err_msg)
    enum_fields = []
    for k, v in all_type.items():
        for field in v.fields():
            if field.get_type()._graphql in enums.keys():
                enum_fields.append(field.get_name())
    enum_fields = util.stable_unique(enum_fields)

    # 生成.h文件
    gen_defines(reqs, resps, mako_dir, defines_out_dir)
    gen_enums(mako_dir, defines_out_dir, enums)
    if server:
        # 生成服务端接口实现文件
        gen_main(mako_dir, schema_out_dir, package)
        gen_servers(req_resp_list, reqs, resps, mako_dir, resolver_out_dir, query_list)
        gen_schema(schema_out_dir, reqs, resps, req_resp_list, mako_dir, query_list)
        gen_tests(req_resp_list, reqs, resps, mako_dir, go_test_dir, query_list, enum_fields)
