#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import util
from enum import Enum


TypeEnum = Enum("TypeEnum", "string int float double time object list list_object enum bool")
enums = []


class Type:
    def __init__(self, kind, _type):
        assert _type
        assert kind in TypeEnum
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
    def __init__(self, name, type_kind, type_type, value, is_necessary, comment):
        self.__name = name
        self.__value = value
        self.__type = Type(type_kind, type_type)
        self.__is_necessary = is_necessary
        self.__comment = comment

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


err_code = Field("error_code", TypeEnum.string, TypeEnum.string, "SUCCESS", True, "错误码")
err_msg = Field("error_msg", TypeEnum.string, TypeEnum.string, "成功", True, "错误信息")


# 根据key, value推导类型
def get_key_attr(name, value):
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

    type_kind, type_type = util.get_type(field_name, value, specified_type)
    # base_type = get_base_type(field_name, value, enums, specified_type)

    return field_name, necessary, comment, type_kind, type_type


class StructInfo:
    def __init__(self, name, is_req, comment):
        self.__fields = []
        self.__name = name
        self.__member_classs = []
        self.__type = util.gen_title_name(name)
        self.__is_req = is_req
        # self.__is_resp = is_resp
        self.__comment = comment

    def add_attribute(self, name, value):
        field_name, necessary, comment, type_kind, type_type = get_key_attr(name, value, enums)
        field = Field(field_name, type_kind, type_type, value, necessary, comment)
        self.add_field(field)

    def add_field(self, field):
        if field not in self.__fields:
            self.__fields.append(field)

    def set_request(self, b):
        self.__is_req = b

    def is_request(self):
        if self.__is_req is None:
            print("未设置对象属于")
            assert False
        return self.__is_req

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def fields(self):
        return self.__fields

    def __eq__(self, value):
        if not value:
            return False
        return self.__name == value.__name

    def __str__(self):
        s = ""
        for field in self.__fields:
            s += str(field) + ' '
        s += "\n"
        return s


class InterfaceInfo:
    def __init__(self, comment, req_st, resp_st):
        self.__comment = comment
        self.__req_st = req_st
        self.__resp_st = resp_st

    def get_comment(self):
        return self.__comment

    def get_req_st(self):
        return self.__req_st

    def get_resp_st(self):
        return self.__resp_st


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
