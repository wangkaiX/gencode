#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from gencode.common import meta
import util
import json

Type = None


def type_go(_type):
    return meta.TypeGo(_type)


def type_cpp(_type):
    return meta.TypeCPP(_type)


def type_graphql(_type):
    return meta.TypeGraphql(_type)


def type_grpc(_type):
    return meta.TypeGrpc


def contain_dict(value):
    if isinstance(value, dict):
        return True
    if isinstance(value, list):
        assert len(value) > 0
        return contain_dict(value[0])
    return False


def __get_list_dict_level(value, level):
    assert contain_dict(value)
    if isinstance(value, list) and contain_dict(value):
        return __get_list_dict_level(value[0], level+1)
    return value, level


def get_list_dict_level(value):
    assert isinstance(value, list) and contain_dict(value)
    return __get_list_dict_level(value, 0)


def is_enum(t):
    if t:
        return t in meta.Enum.types()
    return False


def make_enum(name, note, values):
    assert isinstance(values, list)
    assert not contain_dict(values)
    return meta.Enum(name, note, values)


def make_field(ori_name, value):
    assert not contain_dict(value)
    attrs = split_ori_name(ori_name)
    return meta.Field(*attrs, value)


def make_node(ori_name, value, is_req):
    assert contain_dict(value)
    attrs = split_ori_name(ori_name)
    return meta.Node(*attrs, value, is_req)


def split_ori_name(ori_name):
    attrs = [None] * 4
    temps = ori_name.split('|')
    for i in range(len(temps)):
        attrs[i] = temps[i]

    if attrs[1] in ('Y', 'y'):
        attrs[1] = True
    else:
        attrs[1] = False
    return attrs


def save_file(filename, txt):
    # print("filename:", filename)
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filename, 'w') as f:
        f.write(txt)


def go_fmt(filename):
    cmd = "go fmt %s" % filename
    os.system(cmd)


def package_name(abspath, project_path):
    abspath = util.abs_path(abspath)
    project_path = util.abs_path(project_path)
    abspath.index(project_path)
    abspath = abspath[len(project_path):]
    if abspath[0] == '/':
        abspath = abspath[1:]
    return os.path.join(os.path.basename(project_path), abspath)


def dict2json(req):
    json_str = json.dumps(req, separators=(',', ':'), indent=4, ensure_ascii=False)
    beg = 0
    rdquote_index = json_str.find('":', beg)
    while rdquote_index != -1:
        ldquote_index = json_str.rfind('"', 0, rdquote_index)
        assert ldquote_index != -1
        key_end_index = json_str.find('|', ldquote_index, rdquote_index)
        if key_end_index == -1:
            key_end_index = rdquote_index
        json_str = json_str[:key_end_index] + json_str[rdquote_index:]
        rdquote_index = json_str.find('":', key_end_index + 2)
    return json_str
