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
go_graphql = 'go_graphql'
go_grpc = 'go_grpc'
go_gin = 'go_gin'
common = 'common'

framework_types = [go_graphql, go_grpc, go_gin]
http_methods = ['POST', 'GET']
graphql_methods = ['mutation', 'query']

code_types = {}
code_types[common] =     ['string',      'int32',   'float32', 'bool',    'int64',   'float64', 'time',    'file', 'bytes']
code_types[go] =         ['string',      'int32',   'float32', 'bool',    'int64',   'float64', 'int64',   'file', '[]byte']
code_types[cpp] =        ['std::string', 'int32_t', 'float',   'bool',    'int64_t', 'double',  'int64_t', 'file', 'std::vector<int8_t>']
code_types[go_graphql] = ['String',      'Int',     'Float',   'Boolean', 'Int',     'Float',   'Time',    'file', '']
code_types[go_grpc] =    ['string',      'int32',   'float',   'bool',    'int64',   'double',  'int64',   'file', 'bytes']

code_types[go_gin] = code_types[go]


class FieldType:
    def __init__(self, t):
        self.__type = t
        if t in convert:
            t = convert[t]
        self.__lower = t.lower()
        if self.__lower == 'time':
            print("warning!!! time类型, 最好使用int64")

    def get_type(self, code_type):
        if code_type not in code_types:
            print("不支持的编程语言[%s]" % code_type)
            assert False
        try:
            index = code_types[common].index(self.__lower)
            return code_types[code_type][index]
        except ValueError:
            return self.__type

    @property
    def go(self):
        return self.get_type(go)

    @property
    def cpp(self):
        return self.get_type(cpp)

    @property
    def go_graphql(self):
        return self.get_type(go_graphql)

    @property
    def go_grpc(self):
        return self.get_type(go_grpc)
