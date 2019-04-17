#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from data_type import err_code, err_msg, gen_title_name
from mako.template import Template
import util
from read_config import gen_request_response


def gen_define(st, mako_dir, defines_out_dir, is_response=False):
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


def gen_servers(req_resp_list, reqs, resps, mako_dir, server_out_dir, query_list):
    for interface_name, req, resp in req_resp_list:
        req = list(req.values())[0]
        resp = list(resp.values())[0]
        gen_resolver(interface_name, reqs[req.get_name()], resps[resp.get_name()], mako_dir, server_out_dir)
        gen_func(interface_name, reqs[req.get_name()], resps[resp.get_name()], mako_dir, server_out_dir, query_list)


def gen_func(interface_name, req, resp, mako_dir, server_out_dir, query_list):
    if not os.path.exists(server_out_dir):
        os.makedirs(server_out_dir)

    if interface_name in query_list:
        filename = interface_name + "_query"
    else:
        filename = interface_name + "_mutation"
    filepath = server_out_dir + "/" + filename + ".go"
    if os.path.exists(filepath):
        return

    mako_file = mako_dir + "/func.mako"
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding="utf8")

    sfile = open(filepath, "w")
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


def gen_resolver(interface_name, req, resp, mako_dir, server_out_dir):
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


def gen_schema(filename, req_resp_list, mako_dir, query_list):
    mako_file = mako_dir + "/schema.mako"
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding="utf8")
    sfile = open('schema.graphql', "w")
    r_p_list = []
    reqs = []
    resps = []
    for interface_name, req, resp in req_resp_list:
        req = list(req.values())[0]
        reqs.append(req)
        resp = list(resp.values())[0]
        resps.append(resp)
        r_p_list.append([interface_name, req, resp])

    reqs = util.stable_unique(reqs)
    resps = util.stable_unique(resps)

    ctx = {
            "services": r_p_list,
            "reqs": reqs,
            "resps": resps,
            "gen_title_name": util.gen_title_name,
            "enums": [],
            "query_list": query_list,
            }
    sfile.write(t.render(
        **ctx,
        ))


def gen_code(config_dir, filenames, mako_dir, defines_out_dir, server_out_dir, client_out_file, server=None, client=None, query_list=[]):
    req_resp_list = []
    reqs = {}
    resps = {}

    #
    mako_dir = os.path.abspath(mako_dir)
    config_dir = os.path.abspath(config_dir)
    defines_out_dir = os.path.abspath(defines_out_dir)
    server_out_dir = os.path.abspath(server_out_dir)

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
        gen_servers(req_resp_list, reqs, resps, mako_dir, server_out_dir, query_list)
        gen_schema(client_out_file, req_resp_list, mako_dir, query_list)
