#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import copy
from gencode.common import tool
# from abc import abstractmethod
import util


code_cpp = ["CPP", "CXX", "C++"]
code_go = ["GO", "GOLANG"]

proto_http = 'HTTP'
proto_graphql = 'GRAPHQL'
proto_grpc = 'GRPC'


Types = ["string", "int", "float",
         "double", "time",
         "bool"]


class TypeBase:
    __gin_file = 'GINFILE'

    def __init__(self, _type):
        assert _type
        self.__type = _type
        self.__is_enum = _type in [enum.name for enum in Enum.enums()]
        self.__go = _type
        self.__cpp = _type
        self.__graphql = _type
        self.__grpc = _type
        self.set_type(_type)

    def set_type(self, _type):
        if _type == str:
            _type = 'string'
            self.__go = 'string'
            self.__cpp = 'std::string'
            self.__graphql = 'String'
            self.__grpc = 'string'
        elif _type == int:
            _type = 'int32'
            self.__go = 'int32'
            self.__cpp = 'int32_t'
            self.__graphql = 'Int'
            self.__grpc = 'int32'
        elif _type == "int64":
            _type = 'int64'
            self.__go = 'int64'
            self.__cpp = 'int64_t'
            self.__graphql = 'Int'
            self.__grpc = 'int64'
        elif _type == 'float':
            _type = 'float32'
            self.__go = 'float32'
            self.__cpp = 'float'
            self.__graphql = 'Float'
            self.__grpc = 'float'
        elif _type == float:
            _type = 'float64'
            self.__go = 'float64'
            self.__cpp = 'double'
            self.__graphql = 'Float'
            self.__grpc = 'float'
        elif _type == bool:
            _type = 'bool'
            self.__go = 'bool'
            self.__cpp = 'bool'
            self.__graphql = 'Boolean'
            self.__grpc = 'bool'
        elif _type == 'time':
            self.__go = 'time.Time'
            self.__cpp = 'std::string'
            self.__graphql = 'Time'
            self.__grpc = 'string'
        elif _type.upper() == TypeBase.__gin_file:
            _type = _type.upper()
            self.__go = '*multipart.FileHeader'
        else:
            _type = util.gen_upper_camel(_type)
            self.__go = _type
            self.__cpp = _type
            self.__graphql = _type
            self.__grpc = _type
        self.__type = _type

    @property
    def basename(self):
        return self.__type

    @property
    def go(self):
        return self.__go

    @property
    def cpp(self):
        return self.__cpp

    @property
    def graphql(self):
        return self.__graphql

    @property
    def grpc(self):
        return self.__grpc

    @property
    def name(self):
        assert False

    @property
    def is_enum(self):
        return self.__is_enum

    def __str__(self):
        s = "type:[%s] [is_enum:%s]\n" % (self.name, self.is_enum)
        return s


class TypeGo(TypeBase):
    def __init__(self, _type):
        TypeBase.__init__(self, _type)

    @property
    def name(self):
        return self.go


class TypeCPP(TypeBase):
    def __init__(self, _type):
        TypeBase.__init__(self, _type)

    @property
    def name(self):
        return self.cpp


class TypeGraphql(TypeBase):
    def __init__(self, _type):
        TypeBase.__init__(self, _type)

    @property
    def name(self):
        return self.graphql


class TypeProto(TypeBase):
    def __init__(self, _type):
        TypeBase.__init__(self, _type)

    @property
    def name(self):
        return self.grpc


Type = TypeGo


class Protocol:
    def __init__(self, _type):
        self.__type = _type.upper()
        self.__method = "POST"
        self.__url_prefix = ""

    @property
    def type(self):
        return self.__type

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, m):
        self.__method = m.upper()

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, u):
        self.__url = u

    @property
    def url_prefix(self):
        return self.__url_prefix

    @url_prefix.setter
    def url_prefix(self, u):
        self.__url_prefix = u

    def __str__(self):
        return "[%s] [%s]\n" % (self.protocol, self.method)


public = 'PUBLIC'
private = 'PRIVATE'


class Api:
    def __init__(self, name, req, resp, note):
        self.__name = name
        self.__req = req
        self.__resp = resp
        self.__note = note
        # self.__context = None
        # self.__url = None
        # self.__url_param = None
        # self.__method = None

    def req_md_fields(self):
        fields = self.req.fields + tool.md_nodes2fields(self.req.nodes)
        return fields

    def resp_md_fields(self):
        fields = self.resp.fields + tool.md_nodes2fields(self.resp.nodes)
        return fields

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
    def __init__(self):
        self.__full_path = []

    @property
    def full_path(self):
        return self.__full_path

    @full_path.setter
    def full_path(self, p):
        p = copy.deepcopy(p)
        self.__full_path = p

    @property
    def md_full_path(self):
        r = ""
        for p in self.__full_path[2:]:
            r = r + p + "::"
        return r[:-2]

    def append_full_path(self, paths):
        if not isinstance(paths, list):
            paths = [paths]
        for p in paths:
            self.__full_path.append(p)


class Field(Member):
    def __init__(self, name, required, note, _type, value):
        Member.__init__(self)
        self.__name = name
        self.__required = required
        self.__note = note
        self.__index = None
        if not _type:
            _type = util.get_base_type(value)
        self.__ori_type = _type
        self.__value = value
        self.__dimension = 0

        self.__count_dimension(value)
        if self.type.is_enum:
            i = [e.name for e in Enum.enums()].index(self.type.name)
            enum = Enum.enums()[i]
            note = note + ":"
            for pos, value in zip(range(len(enum.values)), enum.values):
                if value.note:
                    note = note + "%s->%s(%s), " % (pos, value.value, value.note)
                else:
                    note = note + "%s->%s, " % (pos, value.value)
            note = note[:-2]
            self.__note = note
        if not self.__note:
            self.__note = self.__name

    def __eq__(self, o):
        return self.name == o.name

    def __count_dimension(self, value):
        if isinstance(value, list):
            self.__dimension = self.__dimension + 1
            self.__count_dimension(value[0])

    @property
    def index(self):
        assert self.__index is not None
        return self.__index

    @index.setter
    def index(self, value):
        assert isinstance(value, int)
        self.__index = value

    @property
    def name(self):
        return self.__name

    @property
    def required(self):
        return self.__required

    @property
    def note(self):
        return self.__note

    @property
    def type(self):
        return Type(self.__ori_type)

    @property
    def value(self):
        return self.__value

    @property
    def dimension(self):
        return self.__dimension

    def __str__(self):
        s = "[%s] [%s] [%s] [%s] [%s] [dim:%s]\n" % (self.name, self.required, self.note, self.type, self.value, self.dimension)
        return s


# field_code = Field("code", True, "", int, 0)
# field_msg = Field("msg", True, "", str, "SUCCESS")


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


class Node(Member):

    __req_nodes = []
    __resp_nodes = []
    __req_resp_nodes = []
    __config_nodes = []

    @staticmethod
    def req_nodes():
        return Node.__req_nodes

    @staticmethod
    def resp_nodes():
        return Node.__resp_nodes

    @staticmethod
    def req_resp_nodes():
        return Node.__req_resp_nodes

    @staticmethod
    def config_nodes():
        return Node.__config_nodes

    @staticmethod
    def merge_nodes(nodes, node):
        try:
            i = nodes.index(node)
            for n in node.nodes:
                nodes[i].add_node(n)
            for f in node.fields:
                nodes[i].add_field(f)
        except ValueError:
            nodes.append(node)

    @staticmethod
    def merge_all_nodes(node):
        node = copy.copy(node)
        if node.attr.is_req or node.attr.is_url_param:
            Node.merge_nodes(Node.req_nodes(), node)
            Node.merge_nodes(Node.req_resp_nodes(), node)
        elif node.attr.is_resp:
            Node.merge_nodes(Node.resp_nodes(), node)
            Node.merge_nodes(Node.req_resp_nodes(), node)
        elif node.attr.is_config:
            Node.merge_nodes(Node.config_nodes(), node)

    @staticmethod
    def clear():
        Node.__req_resp_nodes = []
        Node.__req_nodes = []
        Node.__resp_nodes = []
        # Node.__config_nodes = []

    def __init__(self, name, required, note, _type, value, attr, full_path):
        Member.__init__(self)
        self.append_full_path(full_path)
        self.append_full_path(name)
        # self.node_full_path = self.full_path
        self.__name = name
        self.__required = required
        self.__note = note
        if not _type:
            _type = util.gen_upper_camel(name)
        self.__ori_type = _type
        self.__value = value
        if isinstance(attr, str):
            self.__attr = Attr(attr)
        elif isinstance(attr, Attr):
            self.__attr = attr
        self.__nodes = []
        self.__fields = []
        self.__dimension = 0
        self.__index = None
        self.__curr_child_index = 1

        assert tool.contain_dict(value)
        self.__parse_values(value)
        if not self.__note:
            self.__note = self.__name
        # construct done
        Node.merge_all_nodes(self)

    # @property
    # def md_fields(self):
    #     return tool.md_nodes2fields(self.nodes) + self.fields

    @property
    def url_param(self):
        ret = "?"
        for field in self.fields:
            ret += "%s=%s&" % (field.name, field.value)
        return ret[:-1]

    @property
    def attr(self):
        return self.__attr

    def add_node(self, node):
        node = copy.copy(node)
        assert isinstance(node, Node)
        if node not in self.nodes:
            node.index = self.__curr_child_index
            # node.full_path = self.full_path
            # node.append_full_path(node.name)
            self.nodes.append(node)
            self.__curr_child_index = self.__curr_child_index + 1

    def add_field(self, field):
        # field = copy.copy(field)
        assert isinstance(field, Field)
        if field not in self.fields:
            field.index = self.__curr_child_index
            # field.append_full_path(self.full_path)
            field.full_path = self.full_path
            field.append_full_path(field.name)
            self.fields.append(field)
            self.__curr_child_index = self.__curr_child_index + 1

    @property
    def index(self):
        assert self.__index is not None
        return self.__index

    @index.setter
    def index(self, value):
        assert isinstance(value, int)
        self.__index = value

    @property
    def dimension(self):
        return self.__dimension

    @dimension.setter
    def dimension(self, value):
        assert isinstance(value, int)
        self.__dimension = value

    def __eq__(self, o):
        return self.type.name == o.type.name

    def __str__(self):
        s = "[%s] [%s] [%s] [%s] [%s] [%s]\n" % (self.name, self.required, self.note, self.type, self.value, self.dimension)
        for node in self.nodes:
            s += str(node)
        for field in self.fields:
            s += str(field)
        return s

    def __parse_values(self, value):
        for k, v in value.items():
            if isinstance(v, list) and isinstance(v[0], dict):
                value, level = tool.get_list_dict_level(v)
                node = tool.make_node(k, value, self.attr, self.full_path)
                node.dimension = level
                # node.index = self.__curr_child_index
                # self.__nodes.append(node)
                self.add_node(node)
            elif tool.contain_dict(v):
                node = tool.make_node(k, v, self.attr, self.full_path)
                # node.index = self.__curr_child_index
                # self.__nodes.append(node)
                self.add_node(node)
            else:
                field = tool.make_field(k, v)
                # field.index = self.__curr_child_index
                # self.__fields.append(field)
                self.add_field(field)
            # self.__curr_child_index = self.__curr_child_index + 1

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return Type(self.__ori_type)

    @property
    def required(self):
        return self.__required

    @property
    def note(self):
        return self.__note

    @property
    def value(self):
        return self.__value

    @property
    def nodes(self):
        return self.__nodes

    @property
    def fields(self):
        return self.__fields


class EnumValue:
    def __init__(self, value):
        vs = value.split('|', -1)
        if len(vs) < 2:
            vs.append('')
        self.value = vs[0]
        self.note = vs[1]


class Enum:

    __types = []
    __enums = []

    @staticmethod
    def add_enum(enum):
        Enum.__enums.append(enum)

    @staticmethod
    def enums():
        return Enum.__enums

    @staticmethod
    def clear():
        Enum.__types = []
        Enum.__enums = []

    def __init__(self, name, note, values=[]):
        self.__name = name
        self.__values = []
        for value in values:
            self.__values.append(EnumValue(value))
        self.__note = note
        self.__option = ""
        # Enum.add_(name)

    @property
    def option(self):
        return self.__option

    @option.setter
    def option(self, o):
        self.__option = o

    @property
    def name(self):
        return self.__name

    @property
    def note(self):
        return self.__note

    def add_value(self, value):
        util.assert_unique(self.__values, value)
        self.__values.append(value)

    @property
    def values(self):
        return self.__values


class File:
    def __init__(self, path, name):
        self.__name = name
        self.__path = path

    @property
    def name(self):
        return self.__name

    @property
    def path_name(self):
        return os.path.join(self.__path, self.__name)


# class Config:
#     def __init__(self, name, required, note, _type, value, attr):

class ErrorInfo():
    def __init__(self, code, msg, number):
        self.code = code
        self.msg = msg
        self.number = number

    def __eq__(self, o):
        return self.code == o.code or self.number == o.number
