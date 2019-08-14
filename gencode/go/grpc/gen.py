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
    nodes = meta.Node.all_nodes()
    types = set([node.type.name for node in nodes])
    unique_nodes = []
    # import pdb
    # pdb.set_trace()
    for node in nodes:
        if node.type.name in types:
            unique_nodes.append(node)
            types.remove(node.type.name)

    # pdb.set_trace()
    r = t.render(
        apis=apis,
        nodes=unique_nodes,
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
    filename = "%s.proto" % proto_package_name
    filename = os.path.join(grpc_proto_dir, filename)
    tool.save_file(filename, code)


def gen_service_define(mako_dir, grpc_service_type_name, package_name):
    meta.Type = meta.TypeGo
    mako_file = os.path.join(mako_dir, 'go', 'grpc', 'service_define.go')
    util.assert_file(mako_file)
    t = Template(filename=mako_file)
    r = t.render(
        grpc_service_type_name=grpc_service_type_name,
        package_name=package_name,
            )
    return r


def gen_service_define_file(mako_dir, grpc_api_dir, grpc_service_type_name, package_name):
    code = gen_service_define(mako_dir, grpc_service_type_name, package_name)

    filename = "%s.go" % util.gen_underline_name(grpc_service_type_name)
    filename = os.path.join(grpc_api_dir, filename)
    tool.save_file(filename, code)
    tool.go_fmt(filename)


def gen_api(project_start_path, api, mako_file, grpc_service_type_name, package_name,
            proto_dir, error_package):
    meta.Type = meta.TypeGo
    util.assert_file(mako_file)
    t = Template(filename=mako_file)
    r = t.render(
        api=api,
        grpc_service_type_name=grpc_service_type_name,
        package_name=package_name,
        proto_dir=tool.package_name(proto_dir, project_start_path),
        error_package=error_package,
        gen_upper_camel=util.gen_upper_camel,
        gen_lower_camel=util.gen_lower_camel,
        gen_underline_name=util.gen_underline_name,
            )
    return r


def gen_apis(project_start_path, apis, mako_dir, grpc_service_type_name, package_name, proto_dir, error_package):
    mako_file = os.path.join(mako_dir, 'go', 'grpc', 'api.go')
    r_dict = {}
    for api in apis:
        r_dict[api.name] = gen_api(project_start_path, api, mako_file, grpc_service_type_name, package_name, proto_dir, error_package)
    return r_dict


def gen_apis_file(project_start_path, apis, mako_dir, grpc_api_dir, grpc_service_type_name, grpc_package_name, grpc_proto_dir, error_package):
    code_dict = gen_apis(project_start_path, apis, mako_dir, grpc_service_type_name, grpc_package_name, grpc_proto_dir, error_package)
    for k, v in code_dict.items():
        filename = "%s.go" % util.gen_underline_name(k)
        filename = os.path.join(grpc_api_dir, filename)
        if not os.path.exists(filename):
            tool.save_file(filename, v)
    tool.go_fmt(grpc_api_dir)


def gen_pb_file(make_dir):
    os.chdir(make_dir)
    os.system("make")


def gen_proto_make(mako_dir, package_name):
    mako_file = os.path.join(mako_dir, 'go', 'grpc', 'proto.mak')
    util.assert_file(mako_file)
    t = Template(filename=mako_file)
    r = t.render(
        package_name=package_name,
            )
    return r


def gen_proto_make_file(mako_dir, package_name, grpc_proto_dir):
    code = gen_proto_make(mako_dir, package_name)
    filename = os.path.join(grpc_proto_dir, "makefile")
    tool.save_file(filename, code)


def gen_init_grpc(project_start_path, mako_dir, grpc_api_dir, grpc_proto_dir, grpc_service_name):
    mako_file = os.path.join(mako_dir, 'go', 'grpc', 'init_grpc.go')
    util.assert_file(mako_file)
    t = Template(filename=mako_file)
    r = t.render(
        grpc_service_name=grpc_service_name,
        grpc_api_dir=tool.package_name(grpc_api_dir, project_start_path),
        proto_dir=tool.package_name(grpc_proto_dir, project_start_path),
            )
    return r


def gen_init_grpc_file(project_path, project_start_path, mako_dir, grpc_api_dir, grpc_proto_dir, grpc_service_name):
    code = gen_init_grpc(project_start_path, mako_dir, grpc_api_dir, grpc_proto_dir, grpc_service_name)
    filename = os.path.join(project_path, "cmd", 'init_grpc.go')
    if not os.path.exists(filename):
        tool.save_file(filename, code)
        tool.go_fmt(filename)


def gen_test(project_start_path, mako_dir, api, grpc_proto_dir, grpc_service_name, grpc_ip, grpc_port):
    mako_file = os.path.join(mako_dir, 'go', 'grpc', 'test.go')
    util.assert_file(mako_file)
    t = Template(filename=mako_file)
    r = t.render(
        proto_dir=tool.package_name(grpc_proto_dir, project_start_path),
        json_input=tool.dict2json(api.req.value),
        ip=grpc_ip,
        port=grpc_port,
        grpc_service_name=grpc_service_name,
        api=api,
        gen_upper_camel=util.gen_upper_camel,
            )
    return r


def gen_test_file(project_path, project_start_path, mako_dir, api, grpc_proto_dir, grpc_service_name, grpc_ip, grpc_port):
    code = gen_test(project_start_path, mako_dir, api, grpc_proto_dir, grpc_service_name, grpc_ip, grpc_port)
    filename = os.path.join(project_path, "app", "test_grpc_api", '%s_test.go' % api.name)
    tool.save_file(filename, code)


def gen_tests_file(project_path, project_start_path, mako_dir, apis, grpc_proto_dir, grpc_service_name, grpc_ip, grpc_port):
    for api in apis:
        gen_test_file(project_path, project_start_path, mako_dir, api, grpc_proto_dir, grpc_service_name, grpc_ip, grpc_port)
    tool.go_fmt(os.path.join(project_path, "app", "test_grpc_api"))


def gen_server_file(project_path, project_start_path, apis, mako_dir, proto_package_name, grpc_service_name,
                    grpc_service_type_name,
                    grpc_package_name,
                    grpc_ip,
                    grpc_port,
                    error_package,
                    grpc_proto_dir, grpc_api_dir, service_name, gen_server, gen_client, gen_test):

    gen_proto_file(apis=apis, mako_dir=mako_dir, grpc_proto_dir=grpc_proto_dir, proto_package_name=proto_package_name,
                   proto_service_name=grpc_service_name)

    gen_proto_make_file(mako_dir=mako_dir, package_name=proto_package_name, grpc_proto_dir=grpc_proto_dir)

    gen_pb_file(make_dir=grpc_proto_dir)

    if gen_server:
        gen_service_define_file(mako_dir=mako_dir, grpc_api_dir=grpc_api_dir,
                                grpc_service_type_name=grpc_service_type_name, package_name=grpc_package_name)

        gen_apis_file(project_start_path=project_start_path, apis=apis, mako_dir=mako_dir, grpc_api_dir=grpc_api_dir,
                      grpc_service_type_name=grpc_service_type_name,
                      grpc_package_name=grpc_package_name, grpc_proto_dir=grpc_proto_dir, error_package=error_package)

        gen_init_grpc_file(project_path=project_path, project_start_path=project_start_path, mako_dir=mako_dir, grpc_api_dir=grpc_api_dir,
                           grpc_proto_dir=grpc_proto_dir, grpc_service_name=grpc_service_name)

    if gen_test:
        gen_tests_file(project_path=project_path, project_start_path=project_start_path, mako_dir=mako_dir, apis=apis,
                       grpc_proto_dir=grpc_proto_dir, grpc_service_name=grpc_service_name,
                       grpc_ip=grpc_ip,
                       grpc_port=grpc_port)
