#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import gencode.common.api as api


def contain_object(value):
    return isinstance(value, dict) or \
        (isinstance(value, list) and isinstance(value[0], dict))


def make_enum(name, note, values):
    assert isinstance(values, list)
    return api.Enum(name, note, values)


def make_field(ori_name, value):
    assert not contain_object(value)



def make_node(ori_name, value):
    assert contain_object(value)
