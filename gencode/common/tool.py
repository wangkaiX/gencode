#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import gencode.common.api as api


def contain_object(value):
    return isinstance(value, dict) or \
        (isinstance(value, list) and isinstance(value[0], dict))


def make_enum(name, note, values):
    assert isinstance(values, list)
    assert not contain_object(values)
    return api.Enum(name, note, values)


def make_field(ori_name, value):
    assert not contain_object(value)
    attrs = split_ori_name(ori_name)
    return api.Field(*attrs, value)


def make_node(ori_name, value):
    assert contain_object(value)
    attrs = split_ori_name(ori_name)


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
