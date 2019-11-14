#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import numpy

convert = {}
convert[int] = 'int32'
convert[float] = 'float32'
convert[bool] = 'bool'
convert[str] = 'string'


go = 'go'
cpp = 'cpp'
graphql = 'graphql'
grpc = 'grpc'
go_gin = 'go_gin'
common = 'common'

code_types = [go, cpp]

framework_types = [graphql, grpc, go_gin]

http_methods = ['POST', 'GET']
graphql_methods = ['mutation', 'query']

code_framework_types = {}
code_framework_types[common] =  ['string',      'int32',   'float32', 'bool',    'int64',   'float64', 'time',    'file', 'bytes']
code_framework_types[go] =      ['string',      'int32',   'float32', 'bool',    'int64',   'float64', 'int64',   'file', '[]byte']
code_framework_types[cpp] =     ['std::string', 'int32_t', 'float',   'bool',    'int64_t', 'double',  'int64_t', 'file', 'std::vector<int8_t>']
code_framework_types[graphql] = ['String',      'Int',     'Float',   'Boolean', 'Int',     'Float',   'Time',    'file', '']
code_framework_types[grpc] =    ['string',      'int32',   'float',   'bool',    'int64',   'double',  'int64',   'file', 'bytes']

code_framework_types[go_gin] = code_framework_types[go]


class FieldType:
    def __init__(self, t):
        if t in convert:
            t = convert[t]
        self.__type = t
        self.__lower = t.lower()
        if self.__lower == 'time':
            print("warning!!! time类型, 最好使用int64")

    def get_type(self, code_type):
        if code_type not in code_framework_types.keys():
            print("不支持的编程语言[%s]" % code_type)
            assert False
        try:
            index = code_framework_types[common].index(self.__lower)
            return code_framework_types[code_type][index]
        except ValueError:
            return self.__type

    @property
    def is_time(self):
        return self.__lower == 'time'

    @property
    def is_file(self):
        return self.__lower == 'file'

    @property
    def go(self):
        return self.get_type(go)

    @property
    def cpp(self):
        return self.get_type(cpp)

    @property
    def graphql(self):
        return self.get_type(graphql)

    @property
    def grpc(self):
        return self.get_type(grpc)

    @property
    def name(self):
        return self.get_type(common)

    def __str__(self):
        # print(self.__type)
        return self.__type
