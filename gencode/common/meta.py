#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gencode.common import tool
# from abc import abstractmethod
import util


code_cpp = ["CPP", "CXX", "C++"]
code_go = ["GO", "GOLANG"]

proto_http = 'HTTP'
proto_graphql = 'GRAPHQL'
proto_proto = 'PROTO'


Types = ["string", "int", "float",
         "double", "time",
         "bool"]

Type = None


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
            self.__go = 'string'
            self.__cpp = 'std::string'
            self.__graphql = 'String'
            self.__grpc = 'string'
        elif _type == int:
            self.__go = 'int32'
            self.__cpp = 'int'
            self.__graphql = 'Int'
            self.__grpc = 'int32'
        elif _type == 'float':
            self.__go = 'float32'
            self.__cpp = 'float'
            self.__graphql = 'Float'
            self.__grpc = 'float'
        elif _type == float:
            self.__go = 'float64'
            self.__cpp = 'double'
            self.__graphql = 'Float'
            self.__grpc = 'float'
        elif _type == bool:
            self.__go = 'bool'
            self.__cpp = 'bool'
            self.__graphql = 'Boolean'
            self.__grpc = 'bool'
        elif _type == 'time':
            self.__go = 'time.Time'
            self.__cpp = 'std::string'
            self.__graphql = 'Time'
            self.__grpc = 'string'
        else:
            _type = util.gen_upper_camel(_type)
            self.__go = _type
            self.__cpp = _type
            self.__graphql = _type
            self.__grpc = _type

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
    def __init__(self, name, req, resp, protocols, note):
        self.__name = name
        self.__req = req
        self.__resp = resp
        self.__protocols = []
        for protocol in protocols:
            if protocol[0].upper() == proto_http:
                p = Protocol(*protocol)
            elif protocol[0].upper() == proto_graphql:
                p = Protocol(*protocol)
            elif protocol[0].upper() == proto_proto:
                p = Protocol(protocol[0], None)
            else:
                print("未知的协议[%s]" % protocol)
                assert False
            self.__protocols.append(p)
        self.__note = note

    @property
    def name(self):
        return self.__name

    @property
    def protocols(self):
        return self.__protocols

    @property
    def method(self):
        return self.__method

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
        s = "[%s] [%s] [%s] [%s] [%s]\n" % (self.name, self.protocols, self.note, self.req, self.resp)
        return s


class Field:
    def __init__(self, name, required, note, _type, value):
        self.__name = name
        self.__required = required
        self.__note = note
        if not _type:
            _type = util.get_base_type(value)
        self.__ori_type = _type
        # self.__type = Type(_type)
        self.__value = value
        self.__dimension = 0

        self.__count_dimension(value)

    def __count_dimension(self, value):
        if isinstance(value, list):
            self.__dimension = self.__dimension + 1
            self.__count_dimension(value[0])

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
    def __init__(self, name, required, note, _type, value):
        self.__name = name
        self.__required = required
        self.__note = note
        if not _type:
            _type = util.gen_upper_camel(name)
        self.__ori_type = _type
        # self.__type = None
        self.__value = value
        self.__nodes = []
        self.__fields = []
        self.__dimension = 0

        assert tool.contain_dict(value)
        self.__parse_values(value)

    @property
    def dimension(self):
        return self.__dimension

    def __str__(self):
        s = "[%s] [%s] [%s] [%s] [%s] [%s]\n" % (self.name, self.required, self.note, self.type, self.value, self.dimension)
        for node in self.nodes:
            s += str(node)
        for field in self.fields:
            s += str(field)
        return s

    def __parse_values(self, value):
        if isinstance(value, list) and tool.contain_dict(value):
            self.__dimension = self.__dimension + 1
            return self.__parse_values(value[0])
        for k, v in value.items():
            if tool.contain_dict(v):
                self.__nodes.append(tool.make_node(k, v))
            else:
                self.__fields.append(tool.make_field(k, v))

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

    def add_field(self, field):
        util.assert_unique([field.name for field in self.__fields], field.name)
        self.__fields.append(field)

    def add_node(self, node):
        util.assert_unique([node.name for node in self.__nodes], node.name)
        self.__nodes.append(node)

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
