#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import numpy

convert = {}
convert['int32'] = int
convert['float32'] = float

types = [str, int, float, bool, 'int64', 'float64', 'time', 'file', 'bytes']

language_go = 'go'
language_cpp = 'cpp'
language_graphql = 'graphql'
language_grpc = 'grpc'

language_types = {}
language_types[language_go] = ['string', 'int32', 'float32', 'bool', 'int64', 'float64', 'int64', 'file', '[]byte']
language_types[language_cpp] = ['std::string', 'int32_t', 'float', 'bool', 'int64_t', 'double', 'int64_t', 'file', 'std::vector<int8_t>']
language_types[language_graphql] = ['String', 'Int', 'Float', 'Boolean', 'Int', 'Float', 'Time', 'file', '']
language_types[language_grpc] = ['string', 'int32', 'float', 'bool', 'int64', 'double', 'int64', 'file', 'bytes']


class FieldType:
    def __init__(self, t):
        self.__type = t.lower()
        if self.__type in convert:
            self.__type = convert[t]
        if self.__type == 'time':
            print("warning!!! time类型, 最好使用int64")

    def get_type(self, language):
        if language not in language_types:
            print("不支持的编程语言[%s]" % language)
            assert False
        try:
            index = types.index(self.__type)
            return language_types[language][index]
        except ValueError:
            return self.__type

    @property
    def go(self):
        return self.get_type(language_go)

    @property
    def cpp(self):
        return self.get_type(language_cpp)

    @property
    def graphql(self):
        return self.get_type(language_graphql)

    @property
    def grpc(self):
        return self.get_type(language_grpc)
