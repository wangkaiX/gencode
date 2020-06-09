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
protobuf = 'protobuf'
grpc = 'grpc'
go_gin = 'go_gin'
common = 'common'


# class Cpp:
beast_websocket_async = 'beast_websocket_async'
beast_websocket_sync = 'beast_websocket_sync'

beast_http_sync = 'beast_http_sync'

asio_tcp_async = 'asio_tcp_async'
asio_tcp_sync = 'asio_tcp_sync'

asio_udp_async = 'asio_udp_async'
asio_udp_sync = 'asio_udp_sync'

asio_serialport_async = 'asio_serialport_async'
asio_serialport_sync = 'asio_serialport_sync'


def is_tcp(t):
    return t in [asio_tcp_async, asio_tcp_sync]

def is_udp(t):
    return t in [asio_udp_async, asio_udp_sync]


# class CppAdapt:
nlohmann_json = 'nlohmann_json'
rapid_json = 'rapid_json'
binary = 'binary'

adapt_name = {}
adapt_name[nlohmann_json] = 'adapt_json'
adapt_name[rapid_json] = 'adapt_json'
adapt_name[binary] = 'adapt_binary'

# log
spdlog = 'spdlog'


code_types = {}
code_types[cpp] = [beast_websocket_async, asio_tcp_async]

code_adapt_types = {}
code_adapt_types[cpp] = [binary, rapid_json, binary]

http_methods = ['POST', 'GET']
graphql_methods = ['mutation', 'query']

code_types = {}
code_types[common] =     ['string',      'int32',   'float32', 'bool',    'int64',   'float64', 'time',    'file', 'bytes']
code_types[go] =         ['string',      'int32',   'float32', 'bool',    'int64',   'float64', 'int64',   'file', '[]byte']
code_types[cpp] =        ['std::string', 'int32_t', 'float',   'bool',    'int64_t', 'double',  'int64_t', 'file', 'std::vector<int8_t>']
code_types[graphql] =    ['String',      'Int',     'Float',   'Boolean', 'Int',     'Float',   'Time',    'file', None]
code_types[protobuf] =   ['string',      'int32',   'float',   'bool',    'int64',   'double',  'int64',   'file', 'bytes']

code_types[go_gin] = code_types[go]
code_types[grpc] = code_types[protobuf]


class FieldType:
    def __init__(self, t):
        if t in convert:
            t = convert[t]
        if not isinstance(t, str):
            print("不合法的类型:", t)
            assert False
        self.__type = t
        self.__lower = t.lower()
        if self.__lower == 'time':
            print("warning!!! time类型, 最好使用int64")

    def get_type(self, code_type):
        if code_type not in code_types.keys():
            print("不支持的编程语言[%s]" % code_type)
            assert False
        try:
            index = code_types[common].index(self.__lower)
            t = code_types[code_type][index]
            if not t:
                print("[%s]不支持类型[%s]" % (code_type, code_types[common][index]))
                assert False
            return t
        except ValueError:
            # 自定义类型
            return self.__type

    @property
    def is_time(self):
        return self.__lower == 'time'

    @property
    def is_file(self):
        return self.__lower == 'file'

    @property
    def is_string(self):
        return self.__lower == 'string'

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
    def protobuf(self):
        return self.get_type(protobuf)

    @property
    def name(self):
        return self.get_type(common)

    def __str__(self):
        # print(self.__type)
        return self.__type
