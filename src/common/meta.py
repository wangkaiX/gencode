#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.common import tool
# from src.common import parser
from src.common import enum_type
from src.common import code_type
# from abc import abstractmethod
import util.python.util as util
# from src.common.code_type import FieldType
# import json5
# import copy


class Protocol:
    def __init__(self, tree_map):
        self.__framework_type = None
        self.__apis = []
        self.__configs = []
        self.__default_map = None
        self.__enums = []
        self.__imports = []
        # tree_map = parser.Json5(filename=filename).parser()

        self.__method = None

        # parser
        self.__parser(tree_map)

    def gen_code_file(self, mako_dir, errno_out_file, service_dir, gen_server, gen_client, gen_test, gen_doc, gen_mock, **kwargs):
        pass

    def __parser(self, tree_map):
        self.__parser_protocol(tree_map['protocol'])
        # self.__parser_import(tree_map['import'])
        self.__parser_default(tree_map['default'])
        self.__parser_enum(tree_map['enum'])
        self.__parser_api(tree_map['api'])
        self.__parser_config(tree_map['config'])

    def __parser_protocol(self, protocol_map):
        self.__framework_type = protocol_map['framework_type']
        tool.assert_framework_type(self.__framework_type)
        if self.__framework_type == code_type.go_graphql:
            self.__parser_go_graphql(protocol_map)
        elif self.__framework_type == code_type.go_grpc:
            self.__parser_go_grpc(protocol_map)
        elif self.__framework_type == code_type.go_gin:
            self.__parser_go_gin(protocol_map)

    def __parser_api(self, api_map):
        for k, v in api_map.items():
            self.__apis.append(Api(k, v, self.__default_map))

    def __parser_config(self, config_map):
        for k, v in config_map.items():
            self.__configs.append(Node(None, k, v))

    def __parser_default(self, default_map):
        self.__default_map = default_map
        # for k, v in default_map.items():
        #     self.__defaults.append(Node(k, v))

    def __parser_import(self, import_list):
        for _import in import_list:
            self.__imports.append(_import)

    def __parser_enum(self, enum_map):
        for k, v in enum_map.items():
            self.__enums.append(enum_type.Enum(k, v))

    def __parser_go_graphql(self, proto_map):
        pass
        # self.__method = proto_map['method']
        # tool.assert_graphql_method(self.__method)

    def __parser_go_grpc(self, proto_map):
        pass

    def __parser_go_gin(self, proto_map):
        pass
        # self.__method = proto_map['method']
        # tool.assert_http_method(self.__method)

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
    def __init__(self, name, value_map, default_map):
        self.__name = name
        self.__note = value_map['note']
        self.__req = None
        self.__resp = None
        self.__url_param = None
        self.__context = None
        self.__cookie = None

        self.__url = None
        self.__url_gw_prefix = None
        self.__url_suffix = None
        self.__url_prefix = None
        self.__method = None

        # 接口对内对外
        self.__api_tags = None
        # 文档类别(前端，后台)
        self.__doc_tags = None

        self.__value_map = value_map
        self.__default_map = default_map

        # parser
        self.__parser()

    def __merge_default(self, node, node_name):
        try:
            print(node, node_name, self.__default_map[node_name])
            default_node = Node(None, node_name, self.__default_map[node_name])
            tool.merge_node(node, default_node)
        except KeyError:
            print("[%s]不存在默认节点" % node_name)

    def __parser(self):
        upper_name = util.gen_upper_camel(self.name)
        print(self.__value_map)
        for k, v in self.__value_map.items():
            if 'req' in k:
                self.__req = Node(None, k, v)
                self.__req.type = upper_name + 'Req'
                self.__merge_default(self.__req, 'req')
            elif 'resp' in k:
                self.__resp = Node(None, k, v)
                self.__req.type = upper_name + 'Resp'
                self.__merge_default(self.__req, 'resp')
            elif 'url_param' in k:
                self.__url_param = Node(None, k, v)
                self.__url_param.type = upper_name + 'UrlParam'
                self.__merge_default(self.__req, 'url_param')
            elif 'context' in k:
                self.__context = Node(None, k, v)
                self.__context.type = upper_name + 'Context'
                self.__merge_default(self.__req, 'context')
            elif 'cookie' in k:
                self.__cookie = Node(None, k, v)
                self.__cookie.type = upper_name + 'Cookie'
                self.__merge_default(self.__req, 'cookie')
            elif 'url' == k:
                self.__url = v
            elif 'method' == k:
                self.__method = v
            elif 'api_tags' == k:
                self.__api_tags = v
            elif 'doc_tags' == k:
                self.__doc_tags = v
            elif 'url_gw_prefix' == k:
                self.__url_gw_prefix = v
            elif 'url_prefix' == k:
                self.__url_prefix = v
            elif 'url_suffix' == k:
                self.__url_suffix = v
            else:
                print("不支持的节点类型[%s]" % k)

        if not self.__url:
            url_prefix = self.__url_prefix if self.__url_prefix is not None else tool.get_map_value(self.__default_map, 'url_prefix', '')
            url_suffix = self.__url_suffix if self.__url_suffix is not None else tool.get_map_value(self.__default_map, 'url_suffix', '')
            if not url_suffix:
                url_suffix = self.__name
            url_gw_prefix = self.__url_gw_prefix if self.__url_gw_prefix is not None else tool.get_map_value(self.__default_map, 'url_gw_prefix', '')
            self.__url = tool.url_concat((url_gw_prefix, url_prefix, url_suffix))

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
        s = "[%s] [%s]\n" % (self.name, self.note)
        return s


class Member:
    # def __init__(self, parent, name, required, note, t, value):
    def __init__(self, parent, name, value_map):
        self.__name, self.__required, self.__note, self.__type = tool.split_ori_name(name)
        if parent:
            self.__full_path = parent.full_path + [self.__name]
            # parent.__curr_child_index = parent.__curr_child_index + 1
        else:
            self.__full_path = [self.__name]
        self.__grpc_index = None
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
        assert not isinstance(t, code_type.FieldType)
        self.__type = code_type.FieldType(t)

    @property
    def value_map(self):
        return self.__value_map

    @property
    def dimension(self):
        return self.__dimension


class Field(Member):
    def __init__(self, father, name, value_map):
        Member.__init__(self, father, name, value_map)
        if not self.type:
            self.type = util.get_base_type(value_map)

    def __eq__(self, o):
        return self.name == o.name

    def __str__(self):
        s = "[%s] [%s] [%s] [%s] [%s] [dim:%s]\n" % (self.name, self.required, self.note, self.type, self.value_map, self.dimension)
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
        if not self.type:
            self.type = util.gen_upper_camel(self.name)

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
        member.grpc_index = self.__curr_child_index
        if isinstance(member, Node):
            self.add_node(member)
        elif isinstance(member, Field):
            self.add_field(member)
        else:
            print("Unknown Type:", member)
            assert False
        self.__curr_child_index += 1

    def add_node(self, node):
        if node.name not in [n.name for n in self.nodes]:
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
        value = tool.get_value(self.value_map)
        for k, v in value.items():
            if tool.contain_dict(v):
                member = Node(self, k, v)
            else:
                member = Field(self, k, v)
            self.add_member(member)

    def __eq__(self, o):
        return self.type.name == o.type.name  # and self.__name == o.__name

    def __str__(self):
        s = "[%s] [%s] [%s] [%s] [%s] [%s]\n" % (self.name, self.required, self.note, self.type, self.value_map, self.dimension)
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
