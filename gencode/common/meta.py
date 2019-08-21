#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
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
        elif _type.upper() == 'GINFILE':
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
    def __init__(self, protocol, method):
        self.__protocol = protocol.upper()
        self.__method = None
        if method:
            self.__method = method.upper()

    @property
    def protocol(self):
        return self.__protocol

    @property
    def method(self):
        return self.__method

    def __str__(self):
        return "[%s] [%s]\n" % (self.protocol, self.method)


class Api:
    def __init__(self, name, req, resp, note):
        self.__name = name
        self.__req = req
        self.__resp = resp
        self.__note = note
        # self.__url = None
        # self.__url_param = None
        # self.__method = None

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


class Field:
    def __init__(self, name, required, note, _type, value):
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


class Node:

    __req_nodes = []
    __resp_nodes = []
    __nodes = []

    @staticmethod
    def req_nodes():
        return Node.__req_nodes

    @staticmethod
    def resp_nodes():
        return Node.__resp_nodes

    @staticmethod
    def all_nodes():
        return Node.__nodes

    @staticmethod
    def clear():
        Node.__nodes = []
        Node.__req_nodes = []
        Node.__resp_nodes = []

    def __init__(self, name, required, note, _type, value, is_req):
        self.__name = name
        self.__required = required
        self.__note = note
        if not _type:
            _type = util.gen_upper_camel(name)
        self.__ori_type = _type
        self.__value = value
        self.__is_req = is_req
        self.__nodes = []
        self.__fields = []
        self.__dimension = 0
        self.__index = None
        self.__curr_child_index = 1

        assert tool.contain_dict(value)
        self.__parse_values(value)
        # construct done
        Node.merge_all_nodes(self)

    @property
    def url_param(self):
        ret = "?"
        for field in self.fields:
            ret += "%s=%s&" % (field.name, field.value)
        if len(ret) > 1:
            return ret[:-1]
        return ""

    @property
    def is_req(self):
        return self.__is_req

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
        if node.__is_req:
            Node.merge_nodes(Node.req_nodes(), node)
        else:
            Node.merge_nodes(Node.resp_nodes(), node)
        Node.merge_nodes(Node.all_nodes(), node)

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

    def add_field(self, field):
        if field not in self.fields:
            self.fields.append(field)

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
                node = tool.make_node(k, value, self.__is_req)
                node.dimension = level
                node.index = self.__curr_child_index
                # print("list object:", k, level)
                self.__nodes.append(node)
            elif tool.contain_dict(v):
                node = tool.make_node(k, v, self.__is_req)
                node.index = self.__curr_child_index
                self.__nodes.append(node)
            else:
                field = tool.make_field(k, v)
                field.index = self.__curr_child_index
                self.__fields.append(field)
            self.__curr_child_index = self.__curr_child_index + 1

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

    # @name.setter
    # def name(self, value):
    #     assert self.__name is None
    #     self.__name = value

    # def add_field(self, field):
    #     util.assert_unique([field.name for field in self.__fields], field.name)
    #     self.__fields.append(field)

    # def add_node(self, node):
    #     util.assert_unique([node.name for node in self.__nodes], node.name)
    #     self.__nodes.append(node)

    @property
    def nodes(self):
        return self.__nodes

    @property
    def fields(self):
        return self.__fields


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

    # @staticmethod
    # def add_type(_type):
    #     util.assert_unique(Enum.__types, _type)
    #     Enum.__types.append(_type)
    #     print(str(Enum.__types))

    # @staticmethod
    # def types():
    #     return Enum.__types

    def __init__(self, name, note, values=[]):
        self.__name = name
        self.__values = values
        self.__note = note
        # Enum.add_(name)

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

    # @values.setter
    # def values(self, vs):
    #     assert self.__values == [] or self.__values is None
    #     assert vs
    #     self.__values = vs


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
