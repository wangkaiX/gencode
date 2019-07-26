#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import collections
from gencode_pkg.common import data_type
import json
import os
from collections import OrderedDict
import re
from mako.template import Template
# import pdb


def gen_main(interface_types, out_dir):
    text = """package main
<%
from gencode_pkg.common import data_type
%>
func main() {
% for interface_type in interface_types:
    % if interface_type == data_type.InterfaceEnum.graphql:
    go GraphqlRun()
    % elif interface_type == data_type.InterfaceEnum.restful:
    go RestfulRun()
    % endif
% endfor
    select {}
}

    """
    t = Template(text=text, input_encoding='utf8')
    filename = out_dir + "/main.go"
    # if os.path.exists(filename):
    #     return
    f = open(filename, "w")
    f.write(t.render(
        interface_types=interface_types
        ))
    f.close()


def gen_enums(all_enum, mako_dir, data_type_out_dir):
    check_file(mako_dir)
    if not os.path.exists(data_type_out_dir):
        os.makedirs(data_type_out_dir)

    filepath = data_type_out_dir + "/" + "enums_gen.go"
    mako_file = mako_dir + "/enum.mako"
    t = Template(filename=mako_file, input_encoding="utf8")
    sfile = open(filepath, "w")
    sfile.write(t.render(
        all_enum=all_enum,
        ))

    sfile.close()


def gen_func(interface, mako_dir, out_dir, pro_path, interface_type, query_list=[]):
    resolver = ""
    mako_file = "func.mako"
    if interface_type == data_type.InterfaceEnum.graphql:
        mako_file = "graphql_resolver.mako"
        if interface.get_name() in query_list:
            resolver = "_query"
        else:
            resolver = "_mutation"
    filename = interface.get_name() + resolver

    filepath = "%s/%s.go" % (out_dir, filename)
    if os.path.exists(filepath) and interface_type == data_type.InterfaceEnum.func:
        return

    mako_file = mako_dir + "/" + mako_file
    check_file(mako_file)

    t = Template(filename=mako_file, input_encoding="utf8")
    sfile = open(filepath, "w")
    sfile.write(t.render(
        pro_path=pro_path,
        gen_title_name=gen_title_name,
        interface=interface,
        ))
    sfile.close()


def gen_define(st, pro_path, mako_dir, mako_file, data_type_out_dir):
    package = os.path.basename(data_type_out_dir)
    ctx = {
            "st": st,
            "gen_title_name": gen_title_name,
            "to_underline": to_underline,
            "package": package,
            "pro_path": pro_path,
          }
    mako_file = mako_dir + "/" + mako_file
    check_file(mako_file)
    t = Template(filename=mako_file, input_encoding='utf8')
    # include_dir = defines_out_dir
    if not os.path.exists(data_type_out_dir):
        os.makedirs(data_type_out_dir)

    print("define:", st.get_name())
    data_type_file = "%s/%s.go" % (data_type_out_dir, st.get_name())
    hfile = open(data_type_file, "w")
    hfile.write(t.render(**ctx))
    hfile.close()


def gen_defines(all_type, pro_path, mako_dir, mako_file, data_type_out_dir):
    for st in all_type:
        # if len(st.fields()) != 0 or len(st.get_nodes()) != 0:
        gen_define(st, pro_path, mako_dir, mako_file, data_type_out_dir)


def to_underline(name):
    pos_underline = name.find('_')
    if -1 == pos_underline:
        pos = re.search('[A-Z]', name)
        # pdb.set_trace()
        while pos:
            if pos.start() == 0:
                name = name[0].lower() + name[1:]
            else:
                name = name[0:pos.start()+1].lower() + name[pos.start()+1:]
                name = name[0:pos.start()].lower() + '_' + name[pos.start():]
            pos = re.search('[A-Z]', name)
    return name


def package_name(dirname):
    gosrc = "%s/src/" % (os.environ['GOPATH'])
    # print(dirname, gosrc)
    if dirname.find(gosrc) != -1:
        return dirname[len(gosrc):]
    return dirname


def abs_path(path):
    if path[0] == '~':
        path = os.environ['HOME'] + path[1:]
    return os.path.abspath(path)


def check_file(filename):
    if not os.path.exists(filename):
        print("文件[%s]不存在" % (filename))
        assert False


def readjson(filename):
    # print("json file:", filename)
    json_str = open(filename).read()
    j = json.loads(json_str, object_pairs_hook=OrderedDict)
    return j


def add_interface(all_interface, interfaces):
    if type(interfaces) != list:
        interfaces = [interfaces]
    for interface in interfaces:
        if interface in all_interface:
            print("接口[%s]重复" % (interface.get_name()))
            assert False
        all_interface.append(interface)


def add_struct(all_type, t):
    # print("add_struct:", t.get_name())
    if t not in all_type:
        all_type.append(t)
    else:
        i = all_type.index(t)
        for field in t.fields():
            all_type[i].add_field(field)


def add_enum(all_enum, e):
    if e in all_enum:
        print("枚举[%s]已存在!" % (e.get_name))
        assert False
    all_enum.append(e)


# 生成驼峰类型的类型名
def gen_title_name(name):
    # print("name:", name)
    if -1 == name.find('_'):
        name = name[0].upper() + name[1:]
        return name
    names = name.split('_')
    name = ""
    for n in names:
        name += n.title()
    return name


def stable_unique(l1):
    l2 = []
    for l in l1:
        if l not in l2:
            l2.append(l)
    return l2


def get_type_name(type_name, specified_type):
    if specified_type:
        return specified_type
    return gen_title_name(type_name)


def make_type(type_kind, type_type, specified_type, all_enum):
    if specified_type:
        type_type = specified_type
    all_enum_name = [enum.get_name() for enum in all_enum]
    if type_type in all_enum_name:
        if type_kind == data_type.TypeEnum.list:
            type_kind = data_type.TypeEnum.list_enum
        else:
            type_kind = data_type.TypeEnum.enum
    return data_type.Type(type_kind, type_type)


# 查找最后一级的类型名
# def get_base_type(field_name, field_value, specified_type, all_enum):
#     type_obj = type(field_value)
#     if type_obj == float:
#         return make_type(data_type.TypeEnum.double, data_type.TypeEnum.double, specified_type, all_enum)
#     elif type_obj == str:
#         return make_type(data_type.TypeEnum.string, data_type.TypeEnum.string, specified_type, all_enum)
#     elif type_obj == int:
#         return make_type(data_type.TypeEnum.int, data_type.TypeEnum.int, specified_type, all_enum)
#     elif type_obj == bool:
#         return make_type(data_type.TypeEnum.bool, data_type.TypeEnum.bool, specified_type, all_enum)
#     elif type_obj in(dict, collections.OrderedDict):
#         return make_type(data_type.TypeEnum.object, gen_title_name(field_name), specified_type, all_enum)
#     elif type_obj == list:
#         if type(field_value[0]) in [float, str, bool, int, list]:
#             # return get_base_type(field_name, field_value[0], specified_type, all_enum)
#             return make_type(data_type.TypeEnum.list, get_base_type_enum(field_value[0]), specified_type, all_enum)
#         else:
#             return make_type(data_type.TypeEnum.list_object, gen_title_name(field_name), specified_type, all_enum)
#     else:
#         print("未知类型:", type_obj)
#         assert False


# string int float double time object list list_object enum bool
def get_base_type_enum(field_value):
    type_obj = type(field_value)
    if type_obj == float:
        return data_type.TypeEnum.float
    elif type_obj == str:
        return data_type.TypeEnum.string
    elif type_obj == int:
        return data_type.TypeEnum.int
    elif type_obj == bool:
        return data_type.TypeEnum.bool
    elif type_obj in(dict, collections.OrderedDict):
        assert False
        # return "object"
    elif type_obj == list:
        # if type(field_value[0]) in [float, str, bool, int, list]:
        return get_base_type_enum(field_value[0])
        # else:
        #    return make_type(data_type.TypeEnum.list_object, gen_title_name(field_name), specified_type)
    else:
        print("未知类型:", type_obj)
        assert False


def get_recursive_type(field_name, field_value, specified_type, all_enum):
    type_obj = type(field_value)
    if type_obj == float:
        return make_type(data_type.TypeEnum.double, data_type.TypeEnum.double, specified_type, all_enum)
    elif type_obj == str:
        return make_type(data_type.TypeEnum.string, data_type.TypeEnum.string, specified_type, all_enum)
    elif type_obj == int:
        return make_type(data_type.TypeEnum.int, data_type.TypeEnum.int, specified_type, all_enum)
    elif type_obj == bool:
        return make_type(data_type.TypeEnum.bool, data_type.TypeEnum.bool, specified_type, all_enum)
    elif type_obj in(dict, collections.OrderedDict):
        return make_type(data_type.TypeEnum.object, gen_title_name(field_name), specified_type, all_enum)
    elif type_obj == list:
        if type(field_value[0]) in [float, str, bool, int, list]:
            return make_type(data_type.TypeEnum.list, get_base_type_enum(field_value[0]), specified_type, all_enum)
        else:
            return make_type(data_type.TypeEnum.list_object, gen_title_name(field_name), specified_type, all_enum)
    else:
        print("未知类型:", type_obj)
        assert False


# 根据字段名和字段的值返回字段的类型
def get_type(field_name, field_value, specified_type, all_enum):
    return get_recursive_type(field_name, field_value, specified_type, all_enum)
