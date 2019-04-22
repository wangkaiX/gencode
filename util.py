#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import collections
import data_type
import json
import os
from collections import OrderedDict
import re
import pdb


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


def get_first_value(m):
    vs = list(m.values())
    if len(vs) == 0:
        return None
    else:
        return vs[0]


def abs_path(path):
    if path[0] == '~':
        path = os.environ['HOME'] + path[1:]
    return os.path.abspath(path)


def check_file(filename):
    if not os.path.exists(filename):
        print("文件[%s]不存在" % (filename))
        assert False


def readjson(filename):
    print("json file:", filename)
    json_str = open(filename).read()
    j = json.loads(json_str, object_pairs_hook=OrderedDict)
    return j


def add_struct(to_dict, struct_name):
    if struct_name not in to_dict.keys():
        to_dict[struct_name] = data_type.StructInfo(struct_name)


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


def get_type_name(type_name, specified_type):
    if specified_type:
        return specified_type
    return gen_title_name(type_name)


def make_type(type_name, specified_type):
    return data_type.Type(type_name, specified_type)


# 查找最后一级的类型名
def get_base_type(field_name, field_value, specified_type=None):
    type_obj = type(field_value)
    if type_obj == float:
        return make_type("double", specified_type)
    elif type_obj == str:
        return make_type("string", specified_type)
    elif type_obj == int:
        return make_type("int", specified_type)
    elif type_obj == bool:
        return make_type("bool", specified_type)
    elif type_obj in(dict, collections.OrderedDict):
        return make_type('object', get_type_name(field_name, specified_type))
    elif type_obj == list:
        if type(field_value[0]) in [float, str, bool, int, list]:
            return get_base_type(field_name, field_value[0], specified_type)
        else:
            return make_type('object', get_type_name(field_name, specified_type))
    else:
        print("未知类型:", type_obj)
        assert False


def get_recursive_type(field_name, field_value, specified_type):
    type_obj = type(field_value)
    if type_obj == float:
        return make_type("double", specified_type)
    elif type_obj == str:
        return make_type("string", specified_type)
    elif type_obj == int:
        return make_type("int", specified_type)
    elif type_obj == bool:
        return make_type("bool", specified_type)
    elif type_obj in(dict, collections.OrderedDict):
        return make_type('object', get_type_name(field_name, specified_type))
    elif type_obj == list:
        if type(field_value[0]) in [float, str, bool, int, list]:
            return get_type(field_name, field_value[0], specified_type)
        else:
            return make_type('object', get_type_name(field_name, specified_type))
    else:
        print("未知类型:", type_obj)
        assert False


# 根据字段名和字段的值返回字段的类型
def get_type(field_name, field_value, specified_type):
    type_obj = type(field_value)
    if type_obj == list:
        _type = get_recursive_type(field_name, field_value, specified_type)
        # print(_type)
        return data_type.Type('list', _type)
    else:
        return get_recursive_type(field_name, field_value, specified_type)
