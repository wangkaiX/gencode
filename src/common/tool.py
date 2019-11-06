#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import util.python.util as util
import json
import copy

from gencode.common import meta
from mako.template import Template


def split(text, sep, size):
    rets = [''] * size
    sps = text.split(sep, -1)
    for i, sp in zip(range(len(sps)), sps):
        rets[i] = sp
    return rets


def contain_dict(value):
    if isinstance(value, dict):
        return True
    if isinstance(value, list):
        assert len(value) > 0
        return contain_dict(value[0])
    return False


def get_value(v):
    if isinstance(v, list):
        return get_value(v[0])
    return v


def __get_dimension(obj, n):
    if isinstance(obj, list):
        return __get_dimension(obj[0], n+1)
    return n


def get_dimension(obj):
    return __get_dimension(obj, 0)


def is_enum(enums, t):
    if t:
        return t.name in [enum.name for enum in enums]
    return False


def get_enum_note(enum):
    note = enum.name + ":"
    for pos, value in zip(range(len(enum.values)), enum.values):
        if value.note:
            note = note + "%s->%s(%s), " % (pos, value.value, value.note)
        else:
            note = note + "%s->%s, " % (pos, value.value)
    return note[:-2]


# def make_enum(name, note, values):
#     assert isinstance(values, list)
#     assert not contain_dict(values)
#     return meta.Enum(name, note, values)


# def make_field(ori_name, value):
#     assert not contain_dict(value)
#     attrs = split_ori_name(ori_name)
#     return meta.Field(*attrs, value)


# def make_node(ori_name, value, is_req, full_path):
#     assert contain_dict(value)
#     attrs = split_ori_name(ori_name)
#     return meta.Node(*attrs, value, is_req, full_path)


def split_ori_name(ori_name):
    attrs = split(ori_name, '|', 4)
    if attrs[1] in ('Y', 'y'):
        attrs[1] = True
    else:
        attrs[1] = False
    return attrs


def save_file(filename, txt):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filename, 'wb') as f:
        btxt = bytes(txt, encoding="utf8")
        f.write(btxt)


def go_fmt(filename):
    old_path = os.path.abspath('.')
    if os.path.isdir(filename):
        os.chdir(filename)
        cmd = "go fmt"
    elif os.path.isfile(filename):
        dirname = os.path.dirname(filename)
        os.chdir(dirname)
        filename = os.path.basename(filename)
        cmd = "go fmt %s" % filename
    r = os.popen(cmd)
    r.read()
    # os.system(cmd)
    os.chdir(old_path)


def package_name(abspath, go_src):
    # 支持windows
    go_src = go_src.replace("\\", "/")
    abspath = util.abs_path(abspath)
    abspath = abspath.replace("\\", "/")
    if go_src[-1] == '/':
        go_src = go_src[:-1]
    abspath.index(go_src)
    ret = abspath[len(go_src)+1:]
    return ret


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


def gen_code(mako_file, **kwargs):
    util.assert_file(mako_file)
    t = Template(filename=mako_file, input_encoding='utf8')
    r = t.render(
            **kwargs,
            )
    return r


def gen_code_file(mako_file, output_file, **kwargs):
    code = gen_code(mako_file, **kwargs)
    save_file(output_file, code)


def md_nodes2fields(nodes):
    nodes = copy.copy(nodes)
    field_list = []
    while len(nodes) > 0:
        children = []
        node = nodes[-1]
        nodes.pop()
        _type = "struct"
        if node.dimension > 0:
            _type = "struct[]"
        field = meta.Field(node.name, node.required, node.note, _type, node.value)
        field.full_path = node.full_path
        field_list.append(field)
        for field in node.fields:
            field_list.append(field)
        for node in node.nodes:
            children.append(node)
        nodes = children + nodes

    return field_list


def url_param2text(params):
    ret = "?"
    for field in params:
        ret += "%s=%s&" % (field.name, field.value)
    return ret[:-1]


def append_unique_node(nodes, node):
    if node.name not in [n.name for n in nodes]:
        nodes.append(node)
        return True
    return False


def append_unique_field(node, field):
    if field not in node.fields:
        node.fields.append(field)
        return True
    return False


def append_member(members, member):
    assert isinstance(members, list)
    if member not in members:
        members.append(member)
        return True
    return False


def is_req(reqs, node):
    return node.type.name in [req.type.name for req in reqs]


# def __json2node(father_full_path, father_nodes, father_fields, children, curr_index):
#     for k, v in children.items():
#         if contain_dict(v):
#             node = make_node(k, v, father_full_path)
#             node.index = curr_index
#             assert append_unique_node(father_nodes, node)
#             curr_index = __json2node(node.full_path, node.nodes, node.fields, v, curr_index + 1)
#         else:
#             field = make_field(k, v)
#             field.index = curr_index
#             assert append_unique_field(father_fields, field)
#         curr_index = curr_index + 1
#     return curr_index


# def json2node(father, children, start_index):
#     if father:
#         nodes = father.nodes
#         fields = father.fields
#         father_full_path = father.full_path
#     else:
#         nodes = []
#         fields = []
#         father_full_path = []
#     curr_index = __json2node(father_full_path, nodes, fields, children, start_index)
#     return nodes, fields, curr_index


def markdown_full_path(full_path):
    r = ""
    for p in full_path[2:]:
        r = r + p + "::"
    return r[:-2]
