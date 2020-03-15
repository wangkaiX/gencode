#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import util.python.util as util
import json
import copy

# from src.common import meta
from code_framework.common import type_set
from mako.template import Template


def distinct_str(s, character):
    if not isinstance(s, str):
        print(s)
        assert False

    ret = ''
    pre = ''
    for c in s:
        if c != character or pre != character:
            ret += c
        pre = c
    return ret


def url_concat(*paths):
    url = ''
    for p in paths:
        if isinstance(p, list) or isinstance(p, tuple):
            p = url_concat(*p)
        else:
            p = distinct_str(p, '/')
            if p == '/':
                p = ''
            elif p:
                if p[0] != '/':
                    p = '/' + p
                if p[-1] == '/':
                    p = p[:-1]
        url += p
    return url


def get_map_value(m, paths, default_value):
    paths = paths.split(".")
    # print(paths)
    for p in paths:
        if not isinstance(m, dict) or p not in m.keys():
            return default_value
        m = m[p]
    return m


# 将树结构的节点转换成链表形式，合并同类型节点
def to_nodes(root):
    # assert not isinstance(root, list)
    if not isinstance(root, list):
        nodes = [root]
    else:
        nodes = root
    node_map = {}
    __get_all_nodes(node_map, nodes)
    return list(node_map.values())


def __get_all_nodes(node_map, nodes):
    for node in nodes:
        if node.type.name in node_map.keys():
            node_map[node.type.name] = merge_node(node_map[node.type.name], node)
        else:
            node_map[node.type.name] = node
        __get_all_nodes(node_map, node.nodes)


# 合并两个同类型结点
def merge_node(node_dst, node_from):
    if node_dst.type.name != node_from.type.name and node_from.type.name not in ["Req", "Resp"]:
        print(node_dst.type.name, node_from.type.name)
        assert False
    node = copy.deepcopy(node_dst)
    __merge_node(node, node_from)
    return node


def __merge_node(node_dst, node_from):
    for field in node_from.fields:
        if field not in node_dst.fields:
            node_dst.add_field(field)
    node_names = [n.name for n in node_dst.nodes]
    for node in node_from.nodes:
        if node.name not in node_names:
            node_dst.add_node(node)
        else:
            index = node_names.index(node.name)
            __merge_node(node_dst.nodes[index], node)


def assert_http_method(method):
    if method not in type_set.http_methods:
        print("http 只支持[%s]", type_set.http_methods)
        assert False


def assert_graphql_method(method):
    if method not in type_set.graphql_methods:
        print("graphql 只支持[%s]", type_set.graphql_methods)
        assert False


def assert_field_type(t):
    if t not in type_set.field_types:
        print("暂时支持的编程语言[%s]", type_set.field_types)
        assert False


def assert_adapt_type(code_type, adapt_type):
    if code_type not in type_set.code_adapt_types and adapt_type not in type_set.code_adapt_types[code_type]:
        print("暂时支持的框架类型[%s] 当前[%s][%s]" % (type_set.code_adapt_types, code_type, adapt_type))
        assert False


def assert_framework_type(code_type, framework):
    # print(code_type, framework, type_set.code_framework_types)
    if code_type not in type_set.code_framework_types and framework not in type_set.code_framework_types[code_type]:
        print("暂时支持的框架类型[%s] 当前[%s][%s]" % (type_set.code_framework_types, code_type, framework))
        assert False


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
    return t.name in [enum.name for enum in enums]


def get_enum_note(enum):
    note = ""
    for pos, value in zip(range(len(enum.values)), enum.values):
        if value.note:
            note = note + "%s->%s(%s), " % (pos, value.value, value.note)
        else:
            note = note + "%s->%s, " % (pos, value.value)
    return note[:-2]


def merge_map(map_dst, map_from):
    if map_from is None:
        map_from = {}
    if map_dst is None:
        return map_from
    return {**map_from, **map_dst}


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
        ext = os.path.splitext(filename)
        if len(ext) > 0 and 'go' == ext[-1]:
            go_fmt(filename)


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


def dict_key_clean2json(req):
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


def dict_key_clean(value_map):
    json_str = dict_key_clean2json(value_map)
    # print(json_str)
    return json.loads(json_str)


def dict2json(value_map):
    return json.dumps(value_map, separators=(',', ':'), indent=4, ensure_ascii=False)


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
    return code


def markdown_type(enums, field):
    if is_enum(enums, field.type):
        t = "Enum"
    elif contain_dict(field.value_map):
        t = "Struct"
    else:
        t = field.type.name
    t += "[]" * field.dimension
    return t


def markdown_note(enums, field):
    if "Enum" == markdown_type(enums, field):
        enum_names = [enum.name for enum in enums]
        index = enum_names.index(field.type.name)
        return get_enum_note(enums[index])
    return field.note


def nodes2fields(nodes):
    nodes = copy.deepcopy(nodes)
    field_list = []
    while len(nodes) > 0:
        node = nodes[-1]
        nodes.pop()
        field_list.append(node)
        field_list += node.fields
        nodes += node.nodes

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


'''
def append_member(members, member):
    assert isinstance(members, list)
    if member not in members:
        members.append(member)
        return True
    return False


def is_req(reqs, node):
    return node.type.name in [req.type.name for req in reqs]
'''


def markdown_full_path(full_path):
    r = ""
    for p in full_path[1:]:
        r = r + p + "::"
    return r[:-2]
