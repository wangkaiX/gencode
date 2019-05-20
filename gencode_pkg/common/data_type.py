#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from gencode_pkg.common import util
# from gencode_pkg.common import data_type
from enum import Enum
# import copy


TypeEnum = Enum("TypeEnum", "string int float double time object list list_object enum bool")
# enums = []


class Type:
    def __init__(self, kind, _type):
        assert _type
        assert kind in TypeEnum
        self._type = _type
        self._go = None
        self._cpp = None
        self._graphql = None
        self._kind = kind
        self.set_type(kind, _type)

    def set_type(self, kind, _type):
        if _type == TypeEnum.string:
            self._go = 'string'
            self._cpp = 'std::string'
            self._graphql = 'String'
        elif _type == TypeEnum.int:
            self._go = 'int32'
            self._cpp = 'int'
            self._graphql = 'Int'
        elif _type == TypeEnum.float:
            self._go = 'float32'
            self._cpp = 'float'
            self._graphql = 'Float'
        elif _type == TypeEnum.double:
            self._go = 'float64'
            self._cpp = 'double'
            self._graphql = 'Float'
        elif _type == TypeEnum.bool:
            self._go = 'bool'
            self._cpp = 'bool'
            self._graphql = 'Boolean'
        elif kind == TypeEnum.object or kind == TypeEnum.enum or kind == TypeEnum.list_object:
            self._go = _type
            self._cpp = _type
            self._graphql = _type
        elif _type == TypeEnum.time:
            self._go = 'time.Time'
            self._cpp = 'std::string'
            self._graphql = 'Time'

    def is_object(self):
        return self._kind == TypeEnum.object or self._kind == TypeEnum.list_object

    def is_list_object(self):
        return self._kind == TypeEnum.list_object

    def is_string(self):
        return self._kind == TypeEnum.string

    def is_bool(self):
        return self._type == TypeEnum.bool

    def is_list(self):
        return self._kind == TypeEnum.list or self._kind == TypeEnum.list_object

    def __str__(self):
        return "kind:%s go_type:%s cpp_type:%s graphql_type:%s\n" % (self._kind, self._go, self._cpp, self._graphql)


# 类属性
class Field:
    def __init__(self, name, _type, value, is_necessary, comment):
        self.__name = name
        self.__value = value
        self.__type = _type
        self.__is_necessary = is_necessary
        self.__comment = comment

    def to_json(self):
        m = {}
        m[self.__name] = self.__value
        return json.dumps(m)

    def get_value(self):
        return self.__value

    def get_name(self):
        return self.__name

    def get_comment(self):
        return self.__comment

    def get_type(self):
        return self.__type

    def is_necessary(self):
        return self.__is_necessary

    def is_object(self):
        return self.__type.is_object()

    def is_list(self):
        return self.__type.is_list()

    def __eq__(self, other):
        return self.__name == other.__name

    def __hash__(self):
        return hash(self.__name)

    def __str__(self):
        return str(self.__name) + ' ' + str(self.__type) + ' ' + str(self.__is_necessary)


err_code = Field("error_code", Type(TypeEnum.string, TypeEnum.string), "SUCCESS", True, "错误码")
err_msg = Field("error_msg", Type(TypeEnum.string, TypeEnum.string), "成功", True, "错误信息")


def get_key_attr(name):
    assert name
    finalAttrs = [None, None, None, None]
    attrs = name.split("|")
    for i in range(0, len(attrs)):
        finalAttrs[i] = attrs[i]
    assert finalAttrs[0] is not None
    # 获取用户指定数据
    field_name, necessary, comment, specified_type = finalAttrs

    if necessary == 'Y' or necessary == 'y':
        necessary = True
    else:
        necessary = False
    return field_name, necessary, comment, specified_type


# 根据key, value推导类型
def get_key_value_attr(name, value):
    field_name, necessary, comment, specified_type = get_key_attr(name)
    _type = util.get_type(field_name, value, specified_type)
    # base_type = get_base_type(field_name, value, enums, specified_type)

    return field_name, necessary, comment, _type


class StructInfo:
    def __init__(self, name, comment, is_req=False, is_resp=False):
        self.__fields = []
        self.__comment = None
        self.__name = None
        self.__field_name = None
        if name.find("|") != -1:
            field_name, _, self.comment, specified_type = get_key_attr(name)
            self.__field_name = field_name
            if specified_type:
                self.__name = specified_type
            else:
                self.__name = field_name
        else:
            self.__name = name
            self.__field_name = name
            self.__comment = comment
        self.__nodes = []
        self.__is_necessary = False
        # self.__is_list = None
        self.__is_req = is_req
        self.__is_resp = is_resp
        # self.__map = {}

    def get_nodes(self):
        return self.__nodes

    def to_json(self):
        # m[self.__field_name] = {}
        # self.__map = {}
        # self.__map[self.__field_name] = self.to_map_r(self.__map)
        return json.dumps(self.to_map(), separators=(',', ':'), indent=4, ensure_ascii=False)

    # def to_map(self):
    #     return self.to_map_r()

    def to_map(self):
        m = {}
        # print(self.__fields)
        for field in self.__fields:
            m["%s|%s" % (field.get_name(), field.is_necessary())] = field.get_value()
        for node in self.__nodes:
            if type(node) == list and len(node) > 0:
                m = [n.to_map() for n in node]
            else:
                m["%s|%s" % (node.__field_name, node.__is_necessary)] = node.to_map()
        return m

        # return json.dumps(m)
    # def set_list(self, b):
    #     self.__is_list = b

    # def is_list(self):
    #     return self.__is_list

    def add_attribute(self, name, value, is_list_object):
        field_name, necessary, comment, _type = get_key_value_attr(name, value)
        if is_list_object:
            st = StructInfo(field_name, comment)
            st.__is_necessary = necessary
            print("list_object:[%s][%s]" % (self.__name, st.get_name()))
            if len(self.__nodes) > 0 and type(self.__nodes[-1]) == list:
                if self.__nodes[-1][0].__name == st.__name:
                    self.__nodes[-1].append(st)
            else:
                self.__nodes.append([st])
            return st, True
        elif _type.is_object():
            st = StructInfo(field_name, comment)
            st.__is_necessary = necessary
            self.__nodes.append(st)
            return st, True
            # self.__list = _type.is_list()
        else:
            field = Field(field_name, _type, value, necessary, comment)
            self.add_field(field)
        return None, False

    # def member_classs(self):
    #     return self.__member_classs

    def add_field(self, field):
        if field not in self.__fields:
            self.__fields.append(field)

    def get_comment(self):
        if self.__comment:
            return self.__comment
        return "定义"

    def is_req(self):
        return self.__is_req

    def is_resp(self):
        return self.__is_resp

    def get_name(self):
        return util.gen_title_name(self.__name)

    # def get_type(self):
    #     return self.__type

    def fields(self):
        return self.__fields

    def __eq__(self, value):
        if not value:
            return False
        return self.get_name() == value.get_name()

    def __str__(self):
        s = "%s:%s\n" % (self.__name, "list" if self.__is_list else "not list")
        for field in self.__fields:
            s += str(field) + '\n'
        # s += '\n'
        # for member in self.__member_classs:
        #     s += "%s" % str(member)
        return s


class InterfaceInfo:
    def __init__(self, name):
        self.__name = name
        self.comment = None
        self.req_st = None
        self.resp_st = None
        self._type = None
        self.__sts = []
        self.__enums = []

    def get_enums(self):
        return self.__enums

    def get_name(self):
        return self.__name

    def __eq__(self, th):
        print("interface __eq__")
        return self.__name == th.__name

    def __str__(self):
        return "interfaceinfo:%s\n%s\n%s\n" % (self.comment, str(self.req_st), str(self.resp_st))

    def get_types(self):
        return self.__sts

    def get_comment(self):
        return self.comment

    def get_req(self):
        print(self.__name)
        print(self.req_st.get_name())
        return self.req_st

    def get_resp(self):
        print(self.resp_st.get_name())
        return self.resp_st


class EnumValue:
    def __init__(self, value, comment):
        self.__value = value
        self.__comment = comment

    def __eq__(self, o):
        return self.__value == o.__value

    def get_value(self):
        return self.__value

    def get_comment(self):
        return self.__comment

    def set_comment(self, comment):
        self.__comment = comment


class Enum:
    def __init__(self, name, comment):
        if name.find("|") != -1:
            params = name.split("|", -1)
            self.__name = params[0]
            if len(params) > 1:
                self.__comment = params[1]
        else:
            self.__name = name
            self.__comment = comment
        self.__values = []

    def __eq__(self, o):
        return self.__name == o.__name

    def get_name(self):
        return self.__name

    def add_value(self, v):
        if v in self.__values:
            i = self.__values.index(v)
            if not self.__values[i].get_comment():
                self.__values[i].set_comment(v.get_comment())
        else:
            self.__values.append(v)

    def get_values(self):
        return self.__values

    def get_comment(self):
        if self.__comment:
            return self.__comment
        return ""


# 接口文件的定义
class HeaderFile:
    def __init__(self):
        self.__file_name = None
        self.__interface_name = None
        self.__is_request = None
        self.__class = None
        self.__include_class_names = []

    def set_is_request(self, b):
        self.__is_request = b

    def set_class(self, _class):
        self.__class = _class

    def __str__(self):
        s = self.__file_name + ' ' + self.__interface_name
        return s


class SourceFile:
    def __init__(self):
        self.__file_name = None
        self.__request = None
        self.__response = None
        self.__interface_name = None

    def set_filename_from_interface_filename(self, name):
        name = name.split(".")[0]
        self.__file_name = name + ".cpp"
        self.__interface_name = name

    def set_request(self, r):
        self.__request = r

    def set_response(self, r):
        self.__response = r
