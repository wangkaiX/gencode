#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from mako.template import Template
import util
from gencode.common import meta
from gencode.common import tool


def gen_proto(apis, mako_dir, service_name, package_name):
    meta.Type = meta.TypeProto
    mako_file = os.path.join(mako_dir, 'go', 'grpc', 'grpc.proto')
    util.assert_file(mako_file)
    t = Template(filename=mako_file)
    r = t.render(
        apis=apis,
        nodes=meta.Node.all_nodes(),
        enums=meta.Enum.enums(),
        service_name=service_name,
        package_name=package_name,
        gen_upper_camel=util.gen_upper_camel,
        gen_lower_camel=util.gen_lower_camel,
        gen_underline_name=util.gen_underline_name,
            )
    return r


def gen_proto_file(apis, mako_dir, grpc_proto_dir, proto_service_name, proto_package_name):
    code = gen_proto(apis, mako_dir, proto_service_name, proto_package_name)
    filename = "%s.proto" % util.gen_underline_name(proto_service_name)
    filename = os.path.join(grpc_proto_dir, filename)
    tool.save_file(filename, code)


def gen_service_define(mako_dir, service_name, package_name):
    meta.Type = meta.TypeGo
    mako_file = os.path.join(mako_dir, 'go', 'grpc', 'service_define.go')
    util.assert_file(mako_file)
    t = Template(filename=mako_file)
    r = t.render(
        service_name=service_name,
        package_name=package_name,
            )
    return r


def gen_service_define_file(mako_dir, grpc_pb_dir, service_name, package_name):
    code = gen_service_define(mako_dir, service_name, package_name)

    filename = "%s.go" % util.gen_underline_name(service_name)
    filename = os.path.join(grpc_pb_dir, filename)
    tool.save_file(filename, code)
    tool.go_fmt(filename)


def gen_api(project_path, api, mako_file, service_name, package_name, error_package):
    meta.Type = meta.TypeGo
    util.assert_file(mako_file)
    t = Template(filename=mako_file)
    r = t.render(
        project_path=project_path,
        api=api,
        service_name=service_name,
        package_name=package_name,
        error_package=error_package,
        gen_upper_camel=util.gen_upper_camel,
        gen_lower_camel=util.gen_lower_camel,
        gen_underline_name=util.gen_underline_name,
            )
    return r


def gen_apis(project_path, apis, mako_dir, service_name, package_name, error_package):
    mako_file = os.path.join(mako_dir, 'go', 'grpc', 'api.go')
    r_dict = {}
    for api in apis:
        r_dict[api.name] = gen_api(project_path, api, mako_file, service_name, package_name, error_package)
    return r_dict


def gen_apis_file(project_path, apis, mako_dir, grpc_pb_dir, grpc_service_name, grpc_package_name, error_package):
    code_dict = gen_apis(project_path, apis, mako_dir, grpc_service_name, grpc_package_name, error_package)
    for k, v in code_dict.items():
        filename = "%s.go" % util.gen_underline_name(k)
        filename = os.path.join(grpc_pb_dir, filename)
        tool.save_file(filename, v)
        tool.go_fmt(filename)


def gen_pb(make_dir, grpc_pb_dir):
    os.chdir(make_dir)
    os.system("make")


def gen_server_file(project_path, apis, mako_dir, proto_service_name, proto_package_name, grpc_service_name, grpc_package_name, error_package,
                    grpc_proto_dir, grpc_pb_dir):

    gen_proto_file(apis=apis, mako_dir=mako_dir, grpc_proto_dir=grpc_proto_dir, proto_package_name=proto_package_name,
                   proto_service_name=proto_service_name)

    gen_service_define_file(mako_dir=mako_dir, grpc_pb_dir=grpc_pb_dir, service_name=grpc_service_name, package_name=grpc_package_name)

    gen_apis_file(project_path=project_path, apis=apis, mako_dir=mako_dir, grpc_pb_dir=grpc_pb_dir, grpc_service_name=grpc_service_name,
                  grpc_package_name=grpc_package_name, error_package=error_package)
