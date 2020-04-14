#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from code_framework.common import tool
from code_framework.common.meta import Node
from code_framework.common import enum_type
# from code_framework.common import type_set
from code_framework.common import protocol_parser
# from code_framework.common import generator
import util.python.util as util
# from code_framework.go.gin import gin as go_gin
# import copy


class Framework:
    def __init__(self, service_name, framework, adapt, protocol_filename,
                 heartbeat_interval_second,
                 heartbeat_miss_max,
                 server_ip, server_port,
                 is_server, gen_doc, gen_test,
                 gen_mock,
                 ):
        self.__framework = framework
        self.__adapt = adapt
        self.__protocol_filename = protocol_filename

        self.service_name = service_name
        if is_server:
            self.service_class_name = util.gen_upper_camel("%s_%s" % (service_name, 'server'))
        else:
            self.service_class_name = util.gen_upper_camel("%s_%s" % (service_name, 'client'))
        # config ######
        cfg = {}
        cfg["heartbeat_interval_second"] = heartbeat_interval_second
        cfg["heartbeat_miss_max"] = heartbeat_miss_max
        if server_ip:
            cfg["ip"] = server_ip
        cfg["port"] = server_port
        '''
        self.heartbeat_interval_second = heartbeat_interval_second
        self.heartbeat_miss_max = heartbeat_miss_max
        self.server_ip = server_ip
        self.server_port = server_port
        '''
        self.config = None
        self.config = {}
        self.config[service_name] = cfg
        ###############
        self.is_server = is_server
        # self.__gen_client = gen_client
        # self.__gen_server = gen_server
        self.gen_doc = gen_doc
        self.gen_test = gen_test

        parser = protocol_parser.Parser(protocol_filename)
        self.__tree_map = parser.parse()
        self.__apis = []
        self.__config = None
        self.__default_map = None
        self.__enums = []
        # self.__imports = []
        # 所以的结构类型
        self.__nodes = []
        # self.__node_map = {}

        # self.__method = None

        # parser
        self.__parser(self.__tree_map)

    # @property
    # def service_name(self):
    #     return self.__service_name

    @property
    def command_name(self):
        return self.__tree_map["command_name"]

    @property
    def framework(self):
        return self.__framework

    @property
    def adapt(self):
        return self.__adapt

    @property
    def nodes(self):
        return self.__nodes

    @property
    def has_file(self):
        for api in self.__apis:
            if api.has_file:
                return True
        return False

    @property
    def has_time(self):
        for api in self.__apis:
            if api.has_time:
                return True
        return False

    def gen_code_file(self, **kwargs):
        # mako_dir, errno_out_file, service_dir,
        # gen_server, gen_client, gen_test, gen_doc, gen_mock, **kwargs):
        # generatorManager = generator.GeneratorManager(self.__code_type, self.__framework_type, **kwargs)
        # generatorManager.gen()
        pass

    def __parser(self, tree_map):
        # self.__parser_import(tree_map['import'])
        self.__parser_default(tree_map['default'])
        self.__parser_enum(tree_map['enum'])
        self.__parser_config('config', tree_map)
        self.__parser_api(tree_map['api'])
        self.__parser_nodes()

    def __parser_nodes(self):
        nodes = []
        for api in self.apis:
            nodes += [api.req, api.resp, api.context, api.url_param, api.cookie]
        self.__nodes = tool.to_nodes(nodes)

    def __parser_api(self, api_map):
        for k, v in api_map.items():
            self.__apis.append(Api(k, v, self.__default_map))

    def __parser_config(self, node_name, tree_map):
        self.__config = Node(None, node_name, tree_map[node_name])
        # for k, v in config_map.items():
        #     self.__configs.append(Node(None, k, v))

    def __parser_default(self, default_map):
        self.__default_map = default_map
        # for k, v in default_map.items():
        #     self.__defaults.append(Node(k, v))

    def __parser_import(self, import_list):
        for _import in import_list:
            self.__imports.append(_import)

    def __parser_enum(self, enum_map):
        for k, v in enum_map.items():
            self.__enums.append(enum_type.Enum(k, v))

    def __parser_go_graphql(self, proto_map):
        pass
        # self.__method = proto_map['method']
        # tool.assert_graphql_method(self.__method)

    def __parser_go_grpc(self, proto_map):
        pass

    def __parser_go_gin(self, proto_map):
        pass
        # self.__method = proto_map['method']
        # tool.assert_http_method(self.__method)

    @property
    def apis(self):
        return self.__apis

    # @property
    # def config(self):
    #     return self.__config

    @property
    def enums(self):
        return self.__enums

    @property
    def type(self):
        return self.__type

    def __str__(self):
        return "[%s] [%s]\n" % (self.protocol, self.default)


class Api:
    def __init__(self, name, value_map, default_map):
        self.__name = name
        # self.__note = value_map['note']
        self.__value_map = value_map
        self.__default_map = default_map
        upper_name = util.gen_upper_camel(name)
        self.__req = Node(None, upper_name + "Req", self.get_default('req'))
        self.__resp = Node(None, upper_name + "Resp", self.get_default('resp'))
        self.__url_param = Node(None, upper_name + "UrlParam", self.get_default('url_param'))
        self.__context = Node(None, upper_name + "Context", self.get_default('context'))
        self.__cookie = Node(None, upper_name + "Cookie", self.get_default('cookie'))

        # 本地path
        self.__url_path = None
        self.__gw_url_path = None
        self.__gw_url_prefix = None
        self.__url_suffix = None
        self.__url_prefix = None

        # 如果是http, graphql
        self.__method = None

        # 接口对内对外
        self.__api_tags = []
        # 文档类别(前端，后台)
        self.__doc_tags = []

        # parser
        self.__parser()

    @property
    def command_code(self):
        # print(self.__value_map)
        return self.__value_map["command_code"]

    def get_default(self, name, default_value={}):
        if name not in self.__default_map.keys():
            return default_value
        return self.__default_map[name]

    # 有些通信方式可以传文件，如go gin [http] 可以传文件
    @property
    def has_file(self):
        return self.__req.has_file

    # 是否要用特殊的时间类型，还是统一时间戳
    @property
    def has_time(self):
        return self.__req.has_time or self.__resp.has_time

    def __merge_default(self, node, node_name):
        try:
            # print(node, node_name, self.__default_map[node_name])
            default_node = Node(None, node_name, self.__default_map[node_name])
            node = tool.merge_node(node, default_node)
        except KeyError:
            pass
            # print("[%s]不存在默认节点" % node_name)

    def __parser(self):
        # print(self.__value_map)
        upper_name = util.gen_upper_camel(self.name)
        for k, v in self.__value_map.items():
            if isinstance(v, dict):
                ori_name = k.split('|')[0]
                v = tool.merge_map(v, self.get_default(ori_name))
                # print("v merge:ori_name[%s] v[%s] default[%s]" % (ori_name, v, self.get_default(ori_name)))
            if 'req' in k:
                self.__req = Node(None, k, v)
                self.__req.type = upper_name + "Req"
                self.__merge_default(self.__req, 'req')
                # self.__record_property(self.__req)
            elif 'resp' in k:
                self.__resp = Node(None, k, v)
                self.__resp.type = upper_name + "Resp"
                self.__merge_default(self.__resp, 'resp')
                # self.__record_property(self.__resp)
            elif 'url_param' in k:
                self.__url_param = Node(None, k, v)
                self.__url_param.type = upper_name + "UrlParam"
                self.__merge_default(self.__url_param, 'url_param')
            elif 'context' in k:
                self.__context = Node(None, k, v)
                self.__context.type = upper_name + "Context"
                self.__merge_default(self.__context, 'context')
            elif 'cookie' in k:
                self.__cookie = Node(None, k, v)
                self.__cookie.type = upper_name + "Cookie"
                self.__merge_default(self.__cookie, 'cookie')
            elif 'url' == k:
                self.__url = v
            elif 'method' == k:
                self.__method = v
            elif 'api_tags' == k:
                if not isinstance(v, list):
                    v = [v]
                self.__api_tags = v
            elif 'doc_tags' == k:
                if not isinstance(v, list):
                    v = [v]
                self.__doc_tags = v
            elif 'url_gw_prefix' == k:
                self.__url_gw_prefix = v
            elif 'url_prefix' == k:
                self.__url_prefix = v
            elif 'url_suffix' == k:
                self.__url_suffix = v
            elif 'note' == k:
                self.__note = v
            else:
                print("不支持的节点类型[%s]" % k)

        if not self.__method:
            self.__method = tool.get_map_value(self.__default_map, 'method', 'POST')

        if not self.__url_prefix:
            self.__url_prefix = tool.get_map_value(self.__default_map, 'url_prefix', '')

        if not self.__gw_url_prefix:
            self.__gw_url_prefix = tool.get_map_value(self.__default_map, 'url_gw_prefix', '')

        if not self.__url_suffix:
            self.__url_suffix = self.__name

        if not self.__url_path:
            self.__url_path = tool.url_concat(self.__url_prefix, self.__url_suffix)

        if not self.__gw_url_path:
            self.__gw_url_path = tool.url_concat(self.__gw_url_prefix, self.__url_prefix, self.__url_suffix)

    @property
    def cookie(self):
        return self.__cookie

    @cookie.setter
    def cookie(self, value):
        self.__cookie = value

    @property
    def api_tags(self):
        return self.__api_tags

    # @api_tags.setter
    # def api_tags(self, value):
    #     self.__api_tags = value

    @property
    def doc_tags(self):
        return self.__doc_tags

    # @doc_tag.setter
    # def doc_tags(self, value):
    #     self.__doc_tags = value

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self, ctx):
        self.__context = ctx

    @property
    def name(self):
        return self.__name

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, v):
        self.__method = v

    @property
    def gw_url(self):
        return self.__gw_url

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, v):
        self.__url = v

    @property
    def gw_url_prefix(self):
        return self.__gw_url_prefix

    @gw_url_prefix.setter
    def gw_url_prefix(self, v):
        self.__gw_url_prefix = v

    @property
    def url_param(self):
        return self.__url_param

    @url_param.setter
    def url_param(self, v):
        self.__url_param = v

    @property
    def note(self):
        return self.__note

    @property
    def req(self):
        return self.__req

    @property
    def resp(self):
        return self.__resp

    def __str__(self):
        s = "[%s] [%s]\n" % (self.name, self.note)
        return s


'''
class Member:
    def __init__(self, parent, name, value_map):
        self._name, self._required, self._note, self._type = tool.split_ori_name(name)
        print("member:", self._name, self._required, self._note, self._type)
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
'''
