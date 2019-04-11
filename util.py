#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import collections
import data_type
import json
import os
from collections import OrderedDict


def check_file(filename):
    if not os.path.exists(filename):
        print("文件[%s]不存在" % (filename))
        assert False


def readjson(filename):
    json_str = open(filename).read()
    j = json.loads(json_str, object_pairs_hook=OrderedDict)
    return j


def add_struct(to_dict, class_name):
    if class_name not in to_dict.keys():
        to_dict[class_name] = data_type.StructInfo(class_name)


# 生成驼峰类型的类型名
def gen_title_name(name):
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


def get_base_type(field_name, field_value):
    type_obj = type(field_value)
    if type_obj == float:
        return data_type.Type('double')
    elif type_obj == str:
        return data_type.Type('string')
    elif type_obj == int:
        return data_type.Type('int')
    elif type_obj == bool:
        return data_type.Type('bool')
    elif type_obj in(dict, collections.OrderedDict):
        type_name = gen_title_name(field_name)
        return data_type.Type('object', type_name)
    elif type_obj == list:
        if type(field_value[0]) in [float, str, bool, int, list]:
            type_name = get_base_type(field_name, field_value[0])
        else:
            type_name = gen_title_name(field_name), "object"
        return data_type.Type('object', type_name)
    else:
        print("未知类型:", type_obj)
        assert False


def get_recursive_type(field_name, field_value):
    type_obj = type(field_value)
    if type_obj == float:
        return "double"
    elif type_obj == str:
        return "std::string"
    elif type_obj == int:
        return "int"
    elif type_obj == bool:
        return "bool"
    elif type_obj in(dict, collections.OrderedDict):
        type_name = gen_title_name(field_name)
        return type_name
    elif type_obj == list:
        if type(field_value[0]) in [float, str, bool, int, list]:
            type_name = get_cpp_type(field_name, field_value[0])
        else:
            type_name = gen_title_name(field_name)
        return type_name
    else:
        print("未知类型:", type_obj)
        assert False


# 根据字段名和字段的值返回字段的类型
def get_cpp_type(field_name, field_value):
    type_obj = type(field_value)
    if type_obj == list:
        type_name = get_cpp_recursive_type(field_name, field_value)
        type_name = "std::vector<" + type_name + ">"
        return type_name
    else:
        return get_cpp_recursive_type(field_name, field_value)


def get_graphql_recursive_type(field_name, field_value):
    type_obj = type(field_value)
    if type_obj == float:
        return "double"
    elif type_obj == str:
        return "String"
    elif type_obj == int:
        return "Int"
    elif type_obj == bool:
        return "Boolean"
    elif type_obj in(dict, collections.OrderedDict):
        type_name = gen_title_name(field_name)
        return type_name
    elif type_obj == list:
        if type(field_value[0]) in [float, str, bool, int, list]:
            type_name = get_graphql_type(field_name, field_value[0])
        else:
            type_name = gen_title_name(field_name)
        return type_name
    else:
        print("未知类型:", type_obj)
        assert False


# 根据字段名和字段的值返回字段的类型
def get_graphql_type(field_name, field_value):
    type_obj = type(field_value)
    if type_obj == list:
        type_name = get_graphql_recursive_type(field_name, field_value)
        type_name = "[" + type_name + "]"
        return type_name
    else:
        return get_graphql_recursive_type(field_name, field_value)


def get_go_recursive_type(field_name, field_value):
    type_obj = type(field_value)
    if type_obj == float:
        return "double"
    elif type_obj == str:
        return "string"
    elif type_obj == int:
        return "int32"
    elif type_obj == bool:
        return "bool"
    elif type_obj in(dict, collections.OrderedDict):
        type_name = gen_title_name(field_name)
        return type_name
    elif type_obj == list:
        if type(field_value[0]) in [float, str, bool, int, list]:
            type_name = get_go_type(field_name, field_value[0])
        else:
            type_name = gen_title_name(field_name)
        return type_name
    else:
        print("未知类型:", type_obj)
        assert False


# 根据字段名和字段的值返回字段的类型
def get_go_type(field_name, field_value):
    type_obj = type(field_value)
    if type_obj == list:
        type_name = get_go_recursive_type(field_name, field_value)
        type_name = "[]" + type_name
        return type_name
    else:
        return get_go_recursive_type(field_name, field_value)
