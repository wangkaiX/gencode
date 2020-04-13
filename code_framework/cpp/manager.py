#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from code_framework.common import type_set
from code_framework.common import tool
from code_framework.base.manager import Manager as ManagerBase
from code_framework.cpp.beast_websocket_async import generator as beast_websocket_async_generator
# from data_type import err_code, err_msg, gen_title_name
# from mako.template import Template
# import util.python.util as util
# from read_config import gen_request_response


class Manager(ManagerBase):
    def __init__(self,
                 project_name,
                 # 代码格式模板目录
                 mako_dir,
                 # 项目生成路径
                 service_dir,
                 # 错误码配置文件
                 error_code,
                 # 错误码输出目录
                 error_outdir,
                 doc_outdir,
                 ):
        # xxx/mako/cpp
        ManagerBase.__init__(self, project_name=project_name, code_type=type_set.cpp,
                             mako_dir=mako_dir, service_dir=service_dir, error_code=error_code,
                             error_outdir=error_outdir, doc_outdir=doc_outdir)
        self._mako_dir = os.path.join(self._mako_dir, 'cpp')
        # self._service_dir = service_dir
        self._frameworks = []

    def gen(self):
        for framework in self._frameworks:
            if type_set.beast_websocket_async == framework.framework:
                mako_dir = os.path.join(self._mako_dir, 'beast_websocket_async')
                generator = beast_websocket_async_generator.Generator(mako_dir=mako_dir,
                                                                      service_dir=self._service_dir,
                                                                      framework=framework,
                                                                      )
                generator.gen()

        # types
        self._gen_types()
        self._gen_apis()
        self._gen_init()
        self._gen_main()

    def _gen_main(self):
        mako_file = os.path.join(self._mako_dir, 'main.cpp')
        out_file = os.path.join(self._service_dir, 'main', 'main.cpp')
        tool.gen_code_file(mako_file, out_file,
                           frameworks=self._frameworks,
                           )

    def _gen_init(self):
        pass

    def _gen_types(self):
        mako_file = os.path.join(self._mako_dir, 'types.h')
        out_file = os.path.join(self._service_dir, 'api', 'types.h')
        std_includes = ['vector', 'string']
        enums = []
        nodes = []
        for framework in self._frameworks:
            nodes += framework.nodes

        for framework in self._frameworks:
            enums += framework.enums

        for enum in enums:
            print(enum)
            for value in enum.values:
                print(value)
        tool.gen_code_file(mako_file, out_file,
                           nodes=nodes,
                           std_includes=std_includes,
                           enums=enums,
                           )

    def _gen_apis(self):
        # header
        mako_file = os.path.join(self._mako_dir, 'apis.h')
        out_file = os.path.join(self._service_dir, 'api', 'api.h')
        apis = []
        for framework in self._frameworks:
            apis += framework.apis

        tool.gen_code_file(mako_file, out_file,
                           apis=apis,
                           )

        mako_file = os.path.join(self._mako_dir, 'api.cpp')
        apis = []
        for framework in self._frameworks:
            apis += framework.apis
        for api in apis:
            out_file = os.path.join(self._service_dir, 'api', api.name + '.cpp')
            if not os.path.exists(out_file):
                tool.gen_code_file(mako_file, out_file,
                                   api=api,
                                   )


'''
def gen_header(struct_info, mako_dir, defines_out_dir):
    include_files = []
    for field in struct_info.fields():
        if field.is_object():
            include_files.append("interface/" + field.get_base_type()._cpp + ".h")
        if field.is_list():
            include_files.append("vector")
        if field.is_string():
            include_files.append("string")
    # set为随机无序，导致代码不完全一致而引发重新编译
    include_files = util.stable_unique(include_files)
    ctx = {
            "include_files": include_files,
            "fields": struct_info.fields(),
          }
    mako_file = mako_dir + "/cpp_header.mako"
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding='utf8')
    include_dir = defines_out_dir
    if not os.path.exists(include_dir):
        # os.mkdir(include_dir)
        os.makedirs(include_dir)

    head_file = include_dir + "/" + struct_info.get_type() + ".h"
    # print(head_file)
    hfile = open(head_file, "w")
    hfile.write(t.render(class_name=struct_info.get_type(), **ctx))
    hfile.close()


def gen_headers(reqs, resps, mako_dir, defines_out_dir):
    for k, v in reqs.items():
        gen_header(v, mako_dir, defines_out_dir)
    for k, v in resps.items():
        gen_header(v, mako_dir, defines_out_dir)


def gen_servers(req_resp_list, reqs, resps, mako_dir, server_out_dir):
    for interface_name, req, resp in req_resp_list:
        req = list(req.values())[0]
        resp = list(resp.values())[0]
        gen_server(interface_name, reqs[req.get_name()], resps[resp.get_name()], mako_dir, server_out_dir)


def gen_server(interface_name, req, resp, mako_dir, server_out_dir):
    if not os.path.exists(server_out_dir):
        os.makedirs(server_out_dir)
    mako_file = mako_dir + "/cpp_server.mako"
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding="utf8")
    filename = interface_name + ".cpp"
    sfile = open(server_out_dir + "/" + filename, "w")
    sfile.write(t.render(
        request=req.get_name(),
        response=resp.get_name(),
        class_name=gen_title_name(interface_name),
        struct_request=req.get_type(),
        struct_response=resp.get_type(),
        interface_name=interface_name,
        ))
    sfile.close()


def gen_client(filename, req_resp_list, mako_dir):
    mako_file = mako_dir + "/cpp_client.mako"
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    util.check_file(mako_file)
    t = Template(filename=mako_file, input_encoding="utf8")
    sfile = open(filename, "w")
    include_files = []
    r_p_list = []
    for interface_name, req, resp in req_resp_list:
        req = list(req.values())[0]
        resp = list(resp.values())[0]
        include_files.append(req.get_type() + ".h")
        include_files.append(resp.get_type() + ".h")
        r_p_list.append([interface_name, req, resp])
    include_files = util.stable_unique(include_files)

    ctx = {
            "include_files": include_files,
            "services": r_p_list,
            }
    sfile.write(t.render(
        module_name='ProjectManagerClient',
        **ctx,
        ))


def gen_code(api_dir, filenames, mako_dir, defines_out_dir, server_out_dir, client_out_file, enums, server=None, client=None):
    assert enums is not None
    req_resp_list = []
    reqs = {}
    resps = {}

    #
    mako_dir = os.path.abspath(mako_dir)
    api_dir = os.path.abspath(api_dir)
    defines_out_dir = os.path.abspath(defines_out_dir)
    server_out_dir = os.path.abspath(server_out_dir)

    #

    # 数据整理
    print(filenames)
    for filename in filenames:
        # test_case.gen_test_case(filename)
        basename = os.path.basename(filename)
        interface_name = basename.split(".")[0]
        req, resp = gen_request_response(filename, enums)
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
    gen_headers(reqs, resps, mako_dir, defines_out_dir)
    if server is not None:
        # 生成服务端接口实现文件
        gen_servers(req_resp_list, reqs, resps, mako_dir, server_out_dir)
    if client is not None:
        gen_client(client_out_file, req_resp_list, mako_dir)
'''
