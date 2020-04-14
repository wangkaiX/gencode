#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from code_framework.common import type_set
from code_framework.common import tool
import util.python.util as util
import copy


class Member:
    def __init__(self, parent, name, value_map):
        self._name, self._required, self._note, self._type = tool.split_ori_name(name)
        # print("member:", self._name, self._required, self._note, self._type)
        if parent:
            self._full_path = parent._full_path + [self._name]
        else:
            self._full_path = [self._name]
        print("name[%s], path:%s" % (self._name, self._full_path))
        self._grpc_index = None
        self._parent = parent
        self._value_map = value_map
        self._dimension = tool.get_dimension(value_map)

        # 未完善
        # if self._type:
        #    assert not isinstance(self._type, type_set.FieldType)
        # self._type = type_set.FieldType(self._type)

        if not self._note:
            self._note = self._name

    @property
    def grpc_index(self):
        assert self._grpc_index is not None
        return self._grpc_index

    @property
    def name(self):
        return self._name

    @property
    def required(self):
        return self._required

    @property
    def note(self):
        return self._note

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, t):
        assert not isinstance(t, type_set.FieldType)
        self._type = type_set.FieldType(t)

    @property
    def value_map(self):
        return self._value_map

    @property
    def dimension(self):
        return self._dimension


class Field(Member):
    def __init__(self, father, name, value_map):
        Member.__init__(self, father, name, value_map)
        if not self._type:
            self._type = util.get_base_type(value_map)
        self._type = type_set.FieldType(self._type)

    def __eq__(self, o):
        return self._name == o._name

    @property
    def value(self):
        return self._value_map

    def __str__(self):
        s = "[%s] [%s] [%s] [%s] [%s] [dim:%s]\n" % \
                (self._name, self._required, self._note, self._type, self._value_map, self._dimension)
        return s


class Node(Member):
    def __init__(self, parent, name, value_map):
        if not value_map:
            value_map = {}
        Member.__init__(self, parent, name, value_map)
        assert tool.contain_dict(value_map)
        if not self._type:
            self._type = util.gen_upper_camel(self._name)
        self._type = type_set.FieldType(self._type)

        self.__curr_child_index = 1
        self.__nodes = []
        self.__fields = []
        self.__has_time = False
        self.__has_file = False
        self.__member_names = set()

        self.parser_children()
        self._value_map = tool.dict_key_clean(self._value_map)
        for member in self.__fields + self.__nodes:
            if member.type.is_file:
                del self.value_map[member.name]

    @property
    def has_time(self):
        return self.__has_time

    @property
    def has_file(self):
        return self.__has_file

    def add_member(self, member):
        member = copy.deepcopy(member)
        self.__add_member(member)

    def __add_member(self, member):
        member._grpc_index = self.__curr_child_index
        if isinstance(member, Node):
            self.add_node(member)
        elif isinstance(member, Field):
            self.add_field(member)
        else:
            print("Unknown Type:", member)
            assert False
        self.__curr_child_index += 1
        if member.name in self.__member_names:
            print("类型[%s]有重复的字段名[%s]" % (self.__type.name, member.name))
            assert False
        else:
            self.__member_names.add(member.name)
        # print(member.type, type(member.type), type(member))
        if not self.__has_file and member.type.is_file:
            self.__has_file = True
        if not self.__has_time and member.type.is_time:
            self.__has_time = True

    def add_node(self, node):
        if node._name not in [n.name for n in self.nodes]:
            self.nodes.append(node)
        else:
            print("重复的字段名:", node._name)
            assert False

    def add_field(self, field):
        if field not in self.fields:
            self.fields.append(field)
        else:
            print("重复的字段名:", field._name)
            assert False

    def parser_children(self):
        value = tool.get_value(self._value_map)
        for k, v in value.items():
            if tool.contain_dict(v):
                member = Node(self, k, v)
            else:
                member = Field(self, k, v)
            self.__add_member(member)

    def __eq__(self, o):
        return self.type.name == o.type.name  # and self.__name == o.__name

    def __str__(self):
        s = "[%s] [%s] [%s] [%s] [%s] [%s]\n" % \
            (self._name, self._required, self._note, self._type, self._value_map, self._dimension)
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
