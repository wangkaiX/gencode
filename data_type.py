#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from util import get_type, gen_title_name, get_base_type


class Type:
    def __init__(self, _type, specified_type=None):
        self._type = _type
        self._type_go = None
        self._type_cpp = None
        self._type_graphql = None
        if _type == 'string':
            self._type_go = 'string'
            self._type_cpp = 'std::string'
            self._type_graphql = 'String'
        elif _type == 'float':
            self._type_go = 'float32'
            self._type_cpp = 'float'
            self._type_graphql = 'Float'
        elif _type == 'double':
            self._type_go = 'float64'
            self._type_cpp = 'double'
            self._type_graphql = 'Float'
        elif _type == 'bool':
            self._type_go = 'bool'
            self._type_cpp = 'bool'
            self._type_graphql = 'Boolean'
        elif _type == 'time':
            self._type_go = 'time.Time'
            self._type_cpp = ''
            self._type_graphql = 'Time'
        elif _type == 'object':
            assert specified_type
            self._type_go = specified_type
            self._type_cpp = specified_type
            self._type_graphql = specified_type
        elif _type == 'list':
            assert specified_type
            self._type_go = '[]' + specified_type
            self._type_cpp = 'std::vector<' + specified_type + '>'
            self._type_graphql = '[' + specified_type + ']'


# 类属性
class Field:
    def __init__(self, name, _type, base_type, is_necessary, comment):
        self.__name = name
        self.__type = _type
        self.__base_type = base_type
        self.__is_necessary = is_necessary
        self.__is_object = False
        self.__is_list = False
        self.__is_string = False
        self.__comment = comment

    def get_base_type(self):
        return self.__base_type

    def get_name(self):
        return self.__name

    def get_comment(self):
        return self.__comment

    def get_type(self):
        return self.__type

    def set_string(self, b):
        self.__is_string = b

    def is_string(self):
        return self.__is_string

    def is_necessary(self):
        return self.__is_necessary

    def set_object(self, b):
        self.__is_object = b

    def is_object(self):
        return self.__is_object

    def set_list(self, b):
        self.__is_list = b

    def is_list(self):
        return self.__is_list

    def __eq__(self, other):
        return self.__name == other.__name

    def __hash__(self):
        return hash(self.__name)

    def __str__(self):
        return str(self.__name) + ' ' + str(self.__type) + ' ' + str(self.__is_necessary)


err_code = Field("error_code", "std::string", "string", True, "错误码")
err_msg = Field("error_msg", "std::string",  "string", True, "错误信息")


def get_key_attr(name, value):
    assert name
    finalAttrs = [None, None, None, None]
    attrs = name.split("|")
    for i in range(0, len(attrs)):
        finalAttrs[i] = attrs[i]
    assert finalAttrs[0] is not None
    # 获取用户指定数据
    field_name, necessary, comment, specified_type = finalAttrs
    # print(field_name, necessary, comment, specified_type)

    if necessary == 'Y' or necessary == 'y':
        necessary = True
    else:
        necessary = False

    _type = get_type(field_name, value)
    base_type = get_base_type(field_name, value)
    if specified_type:
        _type = _type.replace(base_type, specified_type, 1)
        base_type = specified_type
        # base_type = data_type.Type("object", specified_type)

    field_name = field_name.lower()
    return field_name, necessary, comment, _type, base_type


class StructInfo:
    def __init__(self, name):
        self.__fields = []
        self.__name = name
        self.__member_classs = []
        self.__type = gen_title_name(name)

    def add_attribute(self, name, value):
        field_name, necessary, comment, _type, base_type = get_key_attr(name, value)

        field = Field(field_name, _type, base_type, necessary, comment)
        if type(value) == list:
            field.set_list(True)
        _, o = get_base_type(name, value)
        field.set_object(is_object(o))
        field.set_string(is_string(o))
        self.add_field(field)

    def add_field(self, field):
        if field not in self.__fields:
            self.__fields.append(field)

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def fields(self):
        return self.__fields

    def __str__(self):
        s = ""
        for field in self.__fields:
            s += str(field) + ' '
        s += "\n"
        return s


def is_object(o):
    return o == "object"


def is_string(o):
    return o == "string"


def is_list(o):
    return o == "list"


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
