#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from util import get_type, gen_title_name, get_base_type


class Type:
    def __init__(self, _type, specified_type=None):
        self._type = _type
        self._type_go = None
        self._type_cpp = None
        self._type_graphql = None
        self._specified_type = specified_type
        if _type == 'object':
            assert specified_type
            self._type_go = specified_type
            self._type_cpp = specified_type
            self._type_graphql = specified_type
            return
        elif _type == 'list':
            assert specified_type
            self._type_go = '[]' + specified_type._type_go
            self._type_cpp = 'std::vector<' + specified_type._type_cpp + '>'
            self._type_graphql = '[' + specified_type._type_graphql + ']'
            return

        if specified_type:
            if specified_type == 'time':
                self._type = specified_type
                self._type_go = 'time.Time'
                self._type_cpp = 'std::string'
                self._type_graphql = 'Time'
                return

            self._type_go = specified_type
            self._type_cpp = specified_type
            self._type_graphql = specified_type
            return

        if _type == 'string':
            self._type_go = 'string'
            self._type_cpp = 'std::string'
            self._type_graphql = 'String'
        elif _type == 'int':
            self._type_go = 'int'
            self._type_cpp = 'int'
            self._type_graphql = 'Int'
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

    def get_type_name(self):
        if self.is_object():
            return self._specified_type
        return self._type

    def is_object(self):
        return self._type == 'object'

    def is_string(self):
        return self._type == 'string'

    def is_bool(self):
        return self._type == 'bool'

    def is_list(self):
        return self._type == 'list'

    def __str__(self):
        return "type:%s\n go_type:%s\n cpp_type:%s\n graphql_type:%s\n" % (self._type, self._type_go, self._type_cpp, self._type_graphql)


# 类属性
class Field:
    def __init__(self, name, _type, base_type, is_necessary, comment):
        self.__name = name
        self.__type = _type
        self.__base_type = base_type
        print("necessary:", name, is_necessary)
        self.__is_necessary = is_necessary
        self.__comment = comment

    def get_base_type(self):
        return self.__base_type.get_type_name()

    def get_name(self):
        return self.__name

    def get_comment(self):
        return self.__comment

    def get_type(self):
        return self.__type

    def is_string(self):
        return self.__base_type.is_string()

    def is_necessary(self):
        return self.__is_necessary

    def is_object(self):
        return self.__base_type.is_object()

    def is_list(self):
        return self.__type.is_list()

    def __eq__(self, other):
        return self.__name == other.__name

    def __hash__(self):
        return hash(self.__name)

    def __str__(self):
        # return "%s %s %s %s %s %s\n" % (self.__name, self.__base_type.get_type_name())
        return str(self.__name) + ' ' + str(self.__type) + ' ' + str(self.__is_necessary)


err_code = Field("error_code", Type("string"), Type("string"), True, "错误码")
err_msg = Field("error_msg", Type("string"), Type("string"), True, "错误信息")


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
    # print(field_name, necessary, comment, specified_type)

    if necessary == 'Y' or necessary == 'y':
        necessary = True
    else:
        necessary = False

    _type = get_type(field_name, value, specified_type)
    base_type = get_base_type(field_name, value, specified_type)

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
