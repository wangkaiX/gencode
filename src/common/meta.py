#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.common import tool
from src.common import parser
from src.common import enum_type
# from abc import abstractmethod
import util.python.util as util
from src.common.code_type import FieldType
# import json5
# import copy


class Protocol:
    def __init__(self, filename):
        self.__protocol = None
        self.__apis = []
        self.__configs = None
        self.__defaults = None
        self.__enums = []
        self.__imports = []
        tree_map = parser.Json5(filename=filename).parser()
        self.__parser(tree_map)

    def __parser(self, tree_map):
        self.__parser_protocol(tree_map['protocol'])
        self.__parser_import(tree_map['import'])
        self.__parser_default(tree_map['default'])
        self.__parser_enum(tree_map['enum'])
        self.__parser_api(tree_map['api'])
        self.__parser_config(tree_map['config'])

    def __parser_protocol(self, protocol_map):
        framework_type = protocol_map['framework_type']
        tool.assert_framework_type(framework_type)
        self.__protocol = framework_type

    def __parser_api(self, api_map):
        for k, v in api_map.items():
            self.__apis.append(Api(k, v))

    def __parser_config(self, config_map):
        for k, v in config_map.items():
            self.__configs.append(Node(k, v))

    def __parser_default(self, default_map):
        for k, v in default_map.items():
            self.__defaults.append(Node(k, v))

    def __parser_import(self, import_list):
        for _import in import_list:
            self.__imports.append(_import)

    def __parser_enum(self, enum_map):
        for k, v in enum_map.items():
            self.__enums.append(enum_type.Enum(k, v))

    def __check_go_graphql(self, arg_map):
        pass

    def __check_go_grpc(self, arg_map):
        pass

    def __check_go(self, arg_map):
        pass

    @property
    def apis(self):
        return self.__apis

    @property
    def config(self):
        return self.__config

    @property
    def enums(self):
        return self.__enums

    @property
    def type(self):
        return self.__type

    def __str__(self):
        return "[%s] [%s]\n" % (self.protocol, self.default)


class Api:
    def __init__(self, name, value_map):
        self.__name = name
        self.__note = value_map['note']
        self.__req = None
        self.__resp = None
        self.__url_param = None
        self.__context = None
        self.__cookie = None

        self.__url = None
        self.__gw_url = None
        self.__method = None

        # 接口对内对外
        self.__api_tags = None
        # 文档类别(前端，后台)
        self.__doc_tags = None

        self.__parser()

        self.__value_map = value_map

    def __parser(self):
        upper_name = tool.gen_upper_camcl(self.name)
        for k, v in self.__value_map.items():
            if 'req' in k:
                self.__req = Node(None, k, v)
                self.__req.type = upper_name + 'Req'
            elif 'resp' in k:
                self.__resp = Node(None, k, v)
                self.__req.type = upper_name + 'Resp'
            elif 'url_param' in k:
                self.__url_param = Node(None, k, v)
                self.__url_param.type = upper_name + 'UrlParam'
            elif 'context' in k:
                self.__context = Node(None, k, v)
                self.__context.type = upper_name + 'Context'
            elif 'cookie' in k:
                self.__cookie = Node(None, k, v)
                self.__cookie.type = upper_name + 'Cookie'
            elif 'url' == k:
                self.__url = v
            elif 'gw_url' == k:
                self.__gw_url = v
            elif 'method' == k:
                self.__method = v
            elif 'api_tags' == k:
                self.__api_tags = v
            elif 'doc_tags' == k:
                self.__doc_tags = v

    @property
    def cookie(self):
        return self.__cookie

    @cookie.setter
    def cookie(self, value):
        self.__cookie = value

    @property
    def api_tag(self):
        return self.__api_tag

    @api_tag.setter
    def api_tag(self, value):
        self.__api_tag = value

    @property
    def doc_tag(self):
        return self.__doc_tag

    @doc_tag.setter
    def doc_tag(self, value):
        self.__doc_tag = value

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self, ctx):
        self.__context = ctx

    @property
    def name(self):
        return self.__name

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, v):
        self.__method = v

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, v):
        self.__url = v

    @property
    def gw_url(self):
        return self.__gw_url

    @gw_url.setter
    def gw_url(self, v):
        self.__gw_url = v

    @property
    def url_param(self):
        return self.__url_param

    @url_param.setter
    def url_param(self, v):
        self.__url_param = v

    @property
    def note(self):
        return self.__note

    @property
    def req(self):
        return self.__req

    @property
    def resp(self):
        return self.__resp

    def __str__(self):
        s = "[%s] [%s] [%s] [%s] [%s]\n" % (self.name, self.note, self.req, self.resp)
        return s


class Member:
    # def __init__(self, parent, name, required, note, t, value):
    def __init__(self, parent, name, value_map):
        self.__name, self.__required, self.__note, self.__type = tool.split_ori_name(name)
        if parent:
            self.__full_path = parent.full_path + [self.__name]
            self.__grpc_index = parent.__curr_child_index
            parent.__curr_child_index = parent.__curr_child_index + 1
        else:
            self.__full_path = [self.__name]
            self.__grpc_index = None
        self.__curr_child_index = 1
        self.__parent = parent
        self.__value_map = value_map
        # if isinstance(attr, str):
        #     self.__attr = Attr(attr)
        # elif isinstance(attr, Attr):
        #     self.__attr = attr
        self.__dimension = tool.get_dimension(value_map)

        # self.__parse_values(value)
        if not self.__note:
            self.__note = self.__name

    @property
    def full_path(self):
        return self.__full_path

    @property
    def grpc_index(self):
        assert self.__grpc_index is not None
        return self.__grpc_index

    @grpc_index.setter
    def grpc_index(self, value):
        assert isinstance(value, int)
        self.__grpc_index = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def required(self):
        return self.__required

    @property
    def note(self):
        return self.__note

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, t):
        assert not isinstance(t, FieldType)
        self.__type = FieldType(t)

    @property
    def value_map(self):
        return self.__value_map

    @property
    def dimension(self):
        return self.__dimension


class Field(Member):
    def __init__(self, father, name, value_map):
        Member.__init__(self, father, name, value_map)
        if not self.__type:
            self.__type = util.get_base_type(value_map)
            self.__type = FieldType(self.__type)

    def __eq__(self, o):
        return self.name == o.name

    def __str__(self):
        s = "[%s] [%s] [%s] [%s] [%s] [dim:%s]\n" % (self.name, self.required, self.note, self.type, self.value, self.dimension)
        return s


'''
class Attr:
    __type_list = ('req', 'resp', 'enum', 'api', 'config', 'url_param', 'context', 'cookie')

    def __init__(self, _type):
        if _type not in Attr.__type_list:
            print(_type)
            assert False
        self.__type = _type

    def __getattr__(self, name):
        assert 'is_' == name[:3] and name[3:] in Attr.__type_list
        return name == ('is_' + self.__type)
'''


class Node(Member):
    # @staticmethod
    # def merge_nodes(nodes, node):
    #     try:
    #         i = nodes.index(node)
    #         for n in node.nodes:
    #             nodes[i].add_node(n)
    #         for f in node.fields:
    #             nodes[i].add_field(f)
    #     except ValueError:
    #         nodes.append(node)

    # @staticmethod
    # def merge_all_nodes(node):
    #     node = copy.copy(node)
    #     if node.attr.is_req or node.attr.is_url_param:
    #         Node.merge_nodes(Node.req_nodes(), node)
    #         Node.merge_nodes(Node.req_resp_nodes(), node)
    #     elif node.attr.is_resp:
    #         Node.merge_nodes(Node.resp_nodes(), node)
    #         Node.merge_nodes(Node.req_resp_nodes(), node)
    #     elif node.attr.is_config:
    #         Node.merge_nodes(Node.config_nodes(), node)

    def __init__(self, parent, name, value_map):
        Member.__init__(self, parent, name, value_map)
        assert tool.contain_dict(value_map)
        if not self.__type:
            self.__type = util.gen_upper_camel(self.__name)
            self.__type = FieldType(self.__type)

        self.__curr_child_index = 1
        self.__nodes = []
        self.__fields = []

        self.parser_children()

    # @property
    # def md_fields(self):
    #     return tool.md_nodes2fields(self.nodes) + self.fields

    # @property
    # def attr(self):
    #     return self.__attr

    def add_member(self, member):
        if isinstance(member, Node):
            self.add_node(member)
        elif isinstance(member, Field):
            self.add_field(member)
        else:
            print("Unknown Type:", member)
            assert False

    def add_node(self, node):
        if node.name not in [n.name for n in self.ndoes]:
            self.nodes.append(node)
        else:
            print("重复的字段名:", node.name)
            assert False

    def add_field(self, field):
        if field not in self.fields:
            self.fields.append(field)
        else:
            print("重复的字段名:", field.name)
            assert False

    def parser_children(self):
        value = tool.get_value(self.__value)
        for k, v in value.items():
            if tool.contain_dict(v):
                member = Node(self, k, v)
            else:
                member = Field(self, k, v)
            self.add_member(member)

    def __eq__(self, o):
        return self.__type.name == o.__type.name  # and self.__name == o.__name

    def __str__(self):
        s = "[%s] [%s] [%s] [%s] [%s] [%s]\n" % (self.name, self.required, self.note, self.type, self.value, self.dimension)
        for node in self.nodes:
            s += str(node)
        for field in self.fields:
            s += str(field)
        return s

    @property
    def nodes(self):
        return self.__nodes

    @property
    def fields(self):
        return self.__fields
