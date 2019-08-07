#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from mako.template import Template
import util
from gencode.common import meta


def gen_proto(apis, mako_file, service_name, package_name):
    meta.Type = meta.TypeProto
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


def gen_service_define(mako_file, service_name, package_name):
    meta.Type = meta.TypeGo
    util.assert_file(mako_file)
    t = Template(filename=mako_file)
    r = t.render(
        service_name=service_name,
        package_name=package_name,
            )
    return r


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


def gen_apis(project_path, apis, mako_file, service_name, package_name, error_package):
    r_dict = {}
    for api in apis:
        r_dict[api.name] = gen_api(project_path, api, mako_file, service_name, package_name, error_package)
    return r_dict


def gen_code(project_path, apis, mako_dir, proto_service_name, proto_package_name, grpc_service_name, grpc_package_name, error_package):
    mako_file = os.path.join(mako_dir, 'go', 'grpc', 'grpc.proto')
    r_proto = gen_proto(apis, mako_file, proto_service_name, proto_package_name)

    mako_file = os.path.join(mako_dir, 'go', 'grpc', 'service_define.go')
    r_service_define = gen_service_define(mako_file, grpc_service_name, grpc_package_name)

    mako_file = os.path.join(mako_dir, 'go', 'grpc', 'api.go')
    r_apis = gen_apis(project_path, apis, mako_file, grpc_service_name, grpc_package_name, error_package)

    return r_proto, r_service_define, r_apis
