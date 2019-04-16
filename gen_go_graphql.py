#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from data_type import err_code, err_msg, gen_title_name
from mako.template import Template
import util
from read_config import gen_request_response


def gen_define(st, mako_dir, defines_out_dir, is_response=False):
    # set为随机无序，导致代码不完全一致而引发重新编译
    # print(st)
    ctx = {
            "st": st,
            "gen_title_name": util.gen_title_name,
            "is_response": is_response,
          }
    mako_file = mako_dir + "/defines.mako"
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding='utf8')
    include_dir = defines_out_dir
    if not os.path.exists(include_dir):
        os.makedirs(include_dir)

    head_file = "%s/%s.go" % (include_dir, st.get_name())
    # print(head_file)
    hfile = open(head_file, "w")
    hfile.write(t.render(**ctx))
    hfile.close()


def gen_defines(reqs, resps, mako_dir, defines_out_dir):
    for k, v in reqs.items():
        gen_define(v, mako_dir, defines_out_dir)
    for k, v in resps.items():
        gen_define(v, mako_dir, defines_out_dir, is_response=True)
    # for interface_name, req, resp in req_resp_list:
    #    gen_define(interface_name, list(req.values())[0], list(resp.values())[0], mako_dir, defines_out_dir)


def gen_servers(req_resp_list, reqs, resps, mako_dir, server_out_dir):
    for interface_name, req, resp in req_resp_list:
        req = list(req.values())[0]
        resp = list(resp.values())[0]
        gen_server(interface_name, reqs[req.get_name()], resps[resp.get_name()], mako_dir, server_out_dir)


def gen_server(interface_name, req, resp, mako_dir, server_out_dir):
    if not os.path.exists(server_out_dir):
        os.makedirs(server_out_dir)
    mako_file = mako_dir + "/resolver.mako"
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding="utf8")
    filename = interface_name + ".go"
    sfile = open(server_out_dir + "/" + filename, "w")
    sfile.write(t.render(
        request=req.get_name(),
        response=resp.get_name(),
        class_name=gen_title_name(interface_name),
        req=req,
        resp=resp,
        struct_request=req.get_type(),
        struct_response=resp.get_type(),
        interface_name=interface_name,
        gen_title_name=util.gen_title_name,
        ))
    sfile.close()


def gen_schema(filename, req_resp_list, mako_dir):
    mako_file = mako_dir + "/schema.mako"
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding="utf8")
    sfile = open('schema.graphql', "w")
    r_p_list = []
    for interface_name, req, resp in req_resp_list:
        req = list(req.values())[0]
        resp = list(resp.values())[0]
        # include_files.append(req.get_type() + ".h")
        # include_files.append(resp.get_type() + ".h")
        r_p_list.append([interface_name, req, resp])
    # include_files = util.stable_unique(include_files)

    ctx = {
            # "include_files": include_files,
            "services": r_p_list,
            "gen_title_name": util.gen_title_name,
            "enums": [],
            }
    sfile.write(t.render(
        # module_name='ProjectManagerClient',
        **ctx,
        ))


def gen_code(config_dir, filenames, mako_dir, defines_out_dir, server_out_dir, client_out_file, server=None, client=None):
    req_resp_list = []
    reqs = {}
    resps = {}

    #
    mako_dir = os.path.abspath(mako_dir)
    config_dir = os.path.abspath(config_dir)
    defines_out_dir = os.path.abspath(defines_out_dir)
    server_out_dir = os.path.abspath(server_out_dir)

    #

    # 数据整理
    # print(filenames)
    for filename in filenames:
        # test_case.gen_test_case(filename)
        basename = os.path.basename(filename)
        interface_name = basename.split(".")[0]
        req, resp = gen_request_response(filename)
        req_resp_list.append([interface_name, req, resp])
        for k, v in req.items():
            util.add_struct(reqs, k)
            for field in v.fields():
                reqs[k].add_field(field)

        for k, v in resp.items():
            util.add_struct(resps, k)
            for field in v.fields():
                resps[k].add_field(field)
            resps[k].add_field(err_code)
            resps[k].add_field(err_msg)

    # 生成.h文件
    gen_defines(reqs, resps, mako_dir, defines_out_dir)
    if server:
        # 生成服务端接口实现文件
        gen_servers(req_resp_list, reqs, resps, mako_dir, server_out_dir)
        gen_schema(client_out_file, req_resp_list, mako_dir)
