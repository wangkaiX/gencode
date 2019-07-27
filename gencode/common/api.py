#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import util


Types = ["string", "int", "float",
         "double", "time",
         "bool"]


class TypeBase:
    def __init__(self, _type, is_enum):
        assert _type
        self.__type = _type
        self.__is_enum = is_enum
        self.__go = _type
        self.__cpp = _type
        self.__graphql = _type
        self.set_type(_type)

    def set_type(self, _type):
        if _type == 'string':
            self.__go = 'string'
            self.__cpp = 'std::string'
            self.__graphql = 'String'
        elif _type == 'int':
            self.__go = 'int32'
            self.__cpp = 'int'
            self.__graphql = 'Int'
        elif _type == 'float':
            self.__go = 'float32'
            self.__cpp = 'float'
            self.__graphql = 'Float'
        elif _type == 'double':
            self.__go = 'float64'
            self.__cpp = 'double'
            self.__graphql = 'Float'
        elif _type == 'bool':
            self.__go = 'bool'
            self.__cpp = 'bool'
            self.__graphql = 'Boolean'
        elif _type == 'time':
            self.__go = 'time.Time'
            self.__cpp = 'std::string'
            self.__graphql = 'Time'

    @property
    def go(self):
        return self.__go

    @property
    def cpp(self):
        return self.__cpp

    @property
    def is_enum(self):
        return self.__is_enum

    def __str__(self):
        return self.__type


class TypeGo:
    def __init__(self, type_base, is_enum=False):
        self.__type_base = type_base

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.__type_base.go


class TypeCPP:
    def __init__(self, type_base, is_enum=False):
        self.__type_base = type_base

    @property
    def name(self):
        return self.__type_base.cpp


class Api:
    def __init__(self, name, req, resp, protocol, method="", note=""):
        self.__name = name
        self.__req = req
        self.__resp = resp
        self.__protocol = protocol
        self.__method = method
        self.__note = note

    @property
    def name(self):
        return self.__name

    @property
    def protocol(self):
        return self.__protocol

    @property
    def method(self):
        return self.__method

    @property
    def note(self):
        return self.__note


class Field:
    def __init__(self, name, required, note, _type, value):
        self.__name = name
        self.__required = required
        self.__note = note
        self.__type = _type
        self.__value = value

    @property
    def name(self):
        return self.__name

    @property
    def required(self):
        return self.__required

    @property
    def type_name(self):
        return self.__type.name

    @property
    def value(self):
        return self.__value


class Node:
    def __init__(self, name, required, note, _type, nodes=[], fields=[]):
        self.__name = name
        self.__required = required
        self.__note = note
        self.__type = _type
        self.__nodes = nodes
        self.__fields = fields

    @property
    def name(self):
        return self.__name

    @property
    def required(self):
        return self.__required

    @property
    def note(self):
        return self.__note

    @name.setter
    def name(self, value):
        assert self.__name is None
        self.__name = value

    def add_field(self, field):
        util.assert_unique(self.__fields, field)
        self.__fields.append(field)

    @property
    def nodes(self):
        return self.__nodes

    @property
    def fields(self):
        return self.__fields


class Enum:
    def __init__(self, name, values=[]):
        self.__name = name
        self.__values = values

    def add_value(self, value):
        util.assert_unique(self.__values, value)
        self.__values.append(value)
