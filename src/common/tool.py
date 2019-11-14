#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import util.python.util as util
import json
import copy

from src.common import meta
from src.common import code_type
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
        print('before p:', p)
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
        print('after p:', p)
        url += p
    return url


def get_map_value(m, paths, default_value):
    paths = paths.split(".")
    print(paths)
    for p in paths:
        if not isinstance(m, dict) or p not in m.keys():
            return default_value
        m = m[p]
    return m


def get_all_nodes(nodes):
    if not isinstance(nodes, list):
        nodes = [nodes]
    node_map = {}
    __get_all_nodes(node_map, nodes)
    return list(node_map.values())


def __get_all_nodes(node_map, nodes):
    for node in nodes:
        if node.type.name in node_map.keys():
            merge_node(node_map[node.type.name], node)
        else:
            node_map[node.type.name] = node
        __get_all_nodes(node_map, node.nodes)


def merge_node(node1, node2):
    for field in node2.fields:
        if field not in node1.fields:
            node1.add_field(field)
    node_names = [n.name for n in node1.nodes]
    for node in node2.nodes:
        if node.name not in node_names:
            node1.add_node(node)
        else:
            index = node_names.index(node.name)
            merge_node(node1.nodes[index], node)


def assert_http_method(method):
    if method not in code_type.http_methods:
        print("http 只支持[%s]", code_type.http_methods)
        assert False


def assert_graphql_method(method):
    if method not in code_type.graphql_methods:
        print("graphql 只支持[%s]", code_type.graphql_methods)
        assert False


def assert_code_type(t):
    if t not in code_type.code_types:
        print("暂时支持的编程语言[%s]", code_type.code_types)
        assert False


def assert_framework_type(t):
    if t not in code_type.framework_types:
        print("暂时支持的框架类型[%s]", code_type.framework_types)
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


def is_enum(enum_names, t):
    return t.name in enum_names


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


def dict_key_clean(value_map):
    json_str = dict2json(value_map)
    print(json_str)
    return json.loads(json_str)


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
    for p in full_path[2:]:
        r = r + p + "::"
    return r[:-2]
