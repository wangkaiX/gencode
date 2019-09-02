#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from mako.template import Template
from gencode.common import util, data_type
from gencode.common.util import gen_defines, gen_func, gen_enums
from gencode.common.read_config import gen_request_response
# import json
import shutil


def gen_servers(all_interface, all_type, common_mako_dir, mako_dir, func_out_dir, resolver_out_dir, pro_path, query_list):
    if not os.path.exists(resolver_out_dir):
        os.makedirs(resolver_out_dir)
    if not os.path.exists(func_out_dir):
        os.makedirs(func_out_dir)
    shutil.copy(mako_dir + "/resolver.go", resolver_out_dir + "/resolver.go")
    for interface in all_interface:
        gen_func(interface, mako_dir, resolver_out_dir, pro_path, data_type.InterfaceEnum.graphql, query_list)
        gen_func(interface, common_mako_dir, func_out_dir, pro_path, data_type.InterfaceEnum.func, query_list)
    for struct_info in all_type:
        if struct_info.is_resp():
            gen_resolver(struct_info, mako_dir, resolver_out_dir, pro_path)


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


def gen_tests(all_interface, mako_dir, go_test_out_dir, pro_path, port, query_list):
    # import pdb; pdb.set_trace()
    for interface in all_interface:
        gen_test(interface, mako_dir, go_test_out_dir, pro_path, port, query_list)


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


def gen_test(interface, mako_dir, go_test_out_dir, pro_path, port, query_list):
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
                name = "all"
            else:
                name = "none"
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


def gen_code_file(mako_dir, gen_server, gen_client, gen_test, gen_doc, **kwargs):

    mako_dir = os.path.join(mako_dir, 'go', 'graphql')

    # enum
    out_file = os.path.join(kwargs['graphql_define_dir'], 'graphql_enum.go')
    tool.gen_code_file(os.path.join(mako_dir, 'enum.go'),
                       out_file,
                       **kwargs)

    # define
    gen_defines_file(os.path.join(mako_dir, 'define.go'),
                     kwargs['graphql_define_dir'],
                     **kwargs)

    if gen_server:
        # router
        out_file = os.path.join(kwargs['restful_api_dir'], "router.go")
        tool.gen_code_file(os.path.join(mako_dir, 'router.go'),
                           out_file,
                           package_restful_api_dir=tool.package_name(kwargs['restful_api_dir'], kwargs['project_start_dir']),
                           package_restful_define_dir=tool.package_name(kwargs['restful_define_dir'], kwargs['project_start_dir']),
                           # package_project_dir=tool.package_name(kwargs['project_dir'], kwargs['project_start_dir']),
                           package_project_dir=os.path.basename(kwargs['project_dir']),
                           **kwargs)
        tool.go_fmt(out_file)

        # define
        gen_defines_file(os.path.join(mako_dir, 'define.go'),
                         kwargs['restful_define_dir'],
                         # package_project_dir=tool.package_name(kwargs['project_dir'], kwargs['project_start_dir']),
                         package_project_dir=os.path.basename(kwargs['project_dir']),
                         **kwargs)

        # apis
        gen_apis_file(os.path.join(mako_dir, 'api.go'),
                      kwargs['restful_api_dir'],
                      package_project_dir=os.path.basename(kwargs['project_dir']),
                      # package_project_dir=tool.package_name(kwargs['project_dir'], kwargs['project_start_dir']),
                      **kwargs)

        # init_restful
        out_file = os.path.join(kwargs['project_dir'], 'cmd', 'init_restful.go')
        # if not os.path.exists(out_file):
        tool.gen_code_file(os.path.join(mako_dir, 'init_restful.go'),
                           out_file,
                           package_restful_api_dir=tool.package_name(kwargs['restful_api_dir'], kwargs['project_start_dir']),
                           package_project_dir=os.path.basename(kwargs['project_dir']),
                           # package_project_dir=tool.package_name(kwargs['project_dir'], kwargs['project_start_dir']),
                           **kwargs,
                           )
        tool.go_fmt(out_file)

    if gen_test:
        # test
        gen_tests_file(os.path.join(mako_dir, 'test.go'),
                       os.path.join(kwargs['restful_api_dir'], 'test_restful'),
                       **kwargs)
