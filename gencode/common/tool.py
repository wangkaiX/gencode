#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from gencode.common import meta

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
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filename, 'w') as f:
        f.write(txt)


def go_fmt(filename):
    cmd = "go fmt %s" % filename
    os.system(cmd)
