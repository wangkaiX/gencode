#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from code_framework.common import tool
from code_framework.common import type_set
from code_framework.common.meta import Node
from code_framework.common import enum_type
# from code_framework.common import error_code
# from code_framework.common import type_set
from code_framework.common import protocol_parser
# from code_framework.common import generator
import util.python.util as util
# from code_framework.go.gin import gin as go_gin
# import copy


class Framework:
    def __init__(self, service_name, network, adapt, protocol_filename,
                 error_code,
                 heartbeat_interval_second,
                 heartbeat_miss_max, no_resp,
                 server_ip, server_port,
                 is_server, gen_doc, gen_test,
                 gen_mock, length_length=None,
                 ):
        self.__network = network
        self.__adapt = adapt
        self.__protocol_filename = protocol_filename
        self.__length_length = length_length
        self.__no_resp = no_resp
        self.__is_server = is_server
        self.__error_code = error_code

        self.__service_name = service_name
        if is_server:
            self.__service_class_name = util.gen_upper_camel("%s_%s" % (service_name, 'server'))
        else:
            self.__service_class_name = util.gen_upper_camel("%s_%s" % (service_name, 'client'))
        # config ######
        cfg = {}
        if heartbeat_interval_second:
            cfg["heartbeat_interval_second"] = heartbeat_interval_second
        if heartbeat_miss_max:
            cfg["heartbeat_miss_max"] = heartbeat_miss_max
        if is_server and server_ip:
            cfg["ip"] = server_ip
        elif not is_server:
            cfg["ip"] = server_ip

        cfg["port"] = server_port
        if type_set.is_tcp(self.__network):
            cfg["length_length"] = self.__length_length
        '''
        self.heartbeat_interval_second = heartbeat_interval_second
        self.heartbeat_miss_max = heartbeat_miss_max
        self.server_ip = server_ip
        self.server_port = server_port
        '''
        self.config = {}
        self.config[service_name] = cfg
        ###############
        self.__is_server = is_server
        # self.__gen_client = gen_client
        # self.__gen_server = gen_server
        self.gen_doc = gen_doc
        self.gen_test = gen_test

        parser = protocol_parser.Parser(protocol_filename)
        self.__tree_map = parser.parse()

        self.__apis = []
        self.__client_apis = []
        self.__server_apis = []

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

    @property
    def error_code(self):
        return self.__error_code

    # @property
    # def service_name(self):
    #     return self.__service_name
    @property
    def adapt_name(self):
        if self.__is_server:
            suffix = 'server'
        else:
            suffix = 'client'
        # return type_set.adapt_name[self._framework.adapt] + suffix
        return "%s_%s_%s" % (type_set.adapt_name[self.__adapt],
                             self.__service_name, suffix)

    @property
    def adapt_class_name(self):
        return util.gen_upper_camel(self.adapt_name)

    @property
    def service_name(self):
        return self.__service_name

    @property
    def service_class_name(self):
        return self.__service_class_name + "Api"

    @property
    def is_server(self):
        return self.__is_server

    @property
    def no_resp(self):
        return self.__no_resp

    @property
    def length_length(self):
        return self.__length_length

    @property
    def command_name(self):
        return self.__tree_map["command_name"]

    @property
    def network(self):
        return self.__network

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
            api = Api(k, v, self.__default_map)
            api.no_resp = self.no_resp
            self.__apis.append(api)
            if api.opposite:
                self.__client_apis.append(api)
            else:
                self.__server_apis.append(api)
        if not self.__is_server:
            self.__server_apis, self.__client_apis = self.__client_apis, self.__server_apis

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

    @property
    def server_apis(self):
        return self.__server_apis

    @property
    def client_apis(self):
        return self.__client_apis

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
        self.__opposite = False
        self.__no_resp = False

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
    def no_resp(self):
        assert self.__no_resp is not None
        return self.__no_resp

    @no_resp.setter
    def no_resp(self, v):
        self.__no_resp = v

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
            elif 'opposite' == k:
                assert isinstance(v, bool)
                self.__opposite = v
            elif 'no_resp' == k:
                assert isinstance(v, bool)
                self.__no_resp = v
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
    def opposite(self):
        return self.__opposite

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

    # def __hash__(self):
    #     return hash(self.__name)

    def __eq__(self, o):
        return self.__name == o.__name

    def __str__(self):
        s = "[%s] [%s]\n" % (self.name, self.note)
        return s
