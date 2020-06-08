#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from code_framework.common import tool
# from code_framework.common import type_set
from code_framework.common.meta import Node
from code_framework.common import enum_type
from code_framework.common import protocol_parser
import util.python.util as util


class ModuleBase:
    def __init__(self, module_name, adapt, protocol_file,
                 mako_dir, module_dir,
                 error_code,
                 no_resp,
                 ip, port,
                 is_server,
                 ):
        self._adapt = adapt
        self._protocol_file = protocol_file
        self._no_resp = no_resp
        self._error_code = error_code
        self._mako_dir = mako_dir
        self._module_dir = module_dir
        self._util_dir = tool.get_util_dir()
        self._is_server = is_server
        if is_server:
            self._module_class_name = util.gen_upper_camel(module_name) + 'Server'
            self._module_class_impl_name = util.gen_upper_camel(module_name) + 'ServerImpl'
        else:
            self._module_class_name = util.gen_upper_camel(module_name) + 'Client'
            self._module_class_impl_name = util.gen_upper_camel(module_name) + 'ClientImpl'

        self._module_name = module_name
        # config ######
        self._config = {}
        config = {}
        config["ip"] = ip
        config["port"] = port

        self._config[module_name] = config
        ###############

        parser = protocol_parser.Parser(protocol_file)
        self._tree_map = parser.parse()

        self._apis = []
        self._request_apis = []
        self._response_apis = []

        self._default_map = None
        self._enums = []
        # self._imports = []
        # 所有的结构类型
        self._nodes = []
        # self._node_map = {}
        # self._method = None

        # parser
        self.__parser(self._tree_map)

    @property
    def error_code(self):
        return self._error_code

    # @property
    # def module_name(self):
    #     return self._module_name

    # @property
    # def adapt_name(self):
    #     if self._is_server:
    #         suffix = 'server'
    #     else:
    #         suffix = 'client'
    #     # return type_set.adapt_name[self._module.adapt] + suffix
    #     return "%s_%s_%s" % (type_set.adapt_name[self._adapt],
    #                          self._module_name, suffix)

    @property
    def adapt_class_name(self):
        return util.gen_upper_camel(self.adapt_name)

    @property
    def module_name(self):
        return self._module_name

    # @property
    # def module_network_class_name(self):
    #     if self.is_server:
    #         if self.network in [type_set.asio_tcp_async]:
    #             suffix = "TcpServer"
    #     else:
    #         if self.network in [type_set.asio_tcp_async]:
    #             suffix = "TcpClient"
    #     return self._module_class_name + suffix

    @property
    def module_class_impl_name(self):
        return self._module_class_impl_name

    @property
    def no_resp(self):
        return self._no_resp

    # @property
    # def length_length(self):
    #     return self._length_length

    @property
    def command_name(self):
        return self._tree_map["command_name"]

    @property
    def network(self):
        return self._network

    @property
    def adapt(self):
        return self._adapt

    @property
    def nodes(self):
        return self._nodes

    @property
    def has_file(self):
        for api in self._apis:
            if api.has_file:
                return True
        return False

    @property
    def has_time(self):
        for api in self._apis:
            if api.has_time:
                return True
        return False

    def gen_code_file(self, **kwargs):
        # mako_dir, errno_out_file, module_dir,
        # gen_server, gen_client, gen_test, gen_doc, gen_mock, **kwargs):
        # generatorManager = generator.GeneratorManager(self._code_type, self._module_type, **kwargs)
        # generatorManager.gen()
        pass

    def __parser(self, tree_map):
        # self.__parser_import(tree_map['import'])
        self.__parser_default(tree_map['default'])
        if 'enum' in tree_map:
            self.__parser_enum(tree_map['enum'])
        if 'config' in tree_map:
            self.parser_config()
        self.__parser_api(tree_map['api'])
        self.__parser_nodes()

    def __parser_nodes(self):
        nodes = []
        for api in self.apis:
            nodes += [api.req, api.resp, api.context, api.url_param, api.cookie]
        self._nodes = tool.to_nodes(nodes)

    def __parser_api(self, api_map):
        for k, v in api_map.items():
            api = Api(k, v, self._default_map)
            api.no_resp = self.no_resp
            self._apis.append(api)
            if api.opposite:
                self._request_apis.append(api)
            else:
                self._response_apis.append(api)
        if not self._is_server:
            self._response_apis, self._request_apis = self._request_apis, self._response_apis

    def parser_config(self):
        node_name = 'config'
        self._config_node = Node(None, node_name, self._tree_map[node_name])
        # for k, v in config_map.items():
        #     self._configs.append(Node(None, k, v))

    def __parser_default(self, default_map):
        self._default_map = default_map
        # for k, v in default_map.items():
        #     self._defaults.append(Node(k, v))

    def __parser_import(self, import_list):
        for _import in import_list:
            self._imports.append(_import)

    def __parser_enum(self, enum_map):
        for k, v in enum_map.items():
            self._enums.append(enum_type.Enum(k, v))

    def __parser_go_graphql(self, proto_map):
        pass
        # self._method = proto_map['method']
        # tool.assert_graphql_method(self._method)

    def __parser_go_grpc(self, proto_map):
        pass

    def __parser_go_gin(self, proto_map):
        pass
        # self._method = proto_map['method']
        # tool.assert_http_method(self._method)

    @property
    def apis(self):
        return self._apis

    @property
    def response_apis(self):
        return util.unique(self._response_apis)

    @property
    def request_apis(self):
        return util.unique(self._request_apis)

    # @property
    # def config(self):
    #     return self._config

    @property
    def enums(self):
        return self._enums

    @property
    def type(self):
        return self._type

    def __str__(self):
        return "[%s] [%s]\n" % (self.protocol, self.default)


class Api:
    def __init__(self, name, value_map, default_map):
        self._name = name
        # self._note = value_map['note']
        self._value_map = value_map
        self._default_map = default_map
        upper_name = util.gen_upper_camel(name)
        self._req = Node(None, upper_name + "Req", self.get_default('req'))
        self._resp = Node(None, upper_name + "Resp", self.get_default('resp'))
        self._url_param = Node(None, upper_name + "UrlParam", self.get_default('url_param'))
        self._context = Node(None, upper_name + "Context", self.get_default('context'))
        self._cookie = Node(None, upper_name + "Cookie", self.get_default('cookie'))
        self._opposite = False
        self._no_resp = False

        # 本地path
        self._url_path = None
        self._gw_url_path = None
        self._gw_url_prefix = None
        self._url_suffix = None
        self._url_prefix = None

        # 如果是http, graphql
        self._method = None

        # 接口对内对外
        self._api_tags = []
        # 文档类别(前端，后台)
        self._doc_tags = []

        # parser
        self.__parser()

    @property
    def no_resp(self):
        assert self._no_resp is not None
        return self._no_resp

    @no_resp.setter
    def no_resp(self, v):
        self._no_resp = v

    @property
    def command_code(self):
        return self._command_code

    def get_default(self, name, default_value={}):
        if name not in self._default_map.keys():
            return default_value
        return self._default_map[name]

    # 有些通信方式可以传文件，如go gin [http] 可以传文件
    @property
    def has_file(self):
        return self._req.has_file

    # 是否要用特殊的时间类型，还是统一时间戳
    @property
    def has_time(self):
        return self._req.has_time or self._resp.has_time

    def __merge_default(self, node, node_name):
        try:
            # print(node, node_name, self._default_map[node_name])
            default_node = Node(None, node_name, self._default_map[node_name])
            node = tool.merge_node(node, default_node)
        except KeyError:
            pass
            # print("[%s]不存在默认节点" % node_name)

    def __parser(self):
        # print(self._value_map)
        upper_name = util.gen_upper_camel(self.name)
        for k, v in self._value_map.items():
            if isinstance(v, dict):
                ori_name = k.split('|')[0]
                v = tool.merge_map(v, self.get_default(ori_name))
                # print("v merge:ori_name[%s] v[%s] default[%s]" % (ori_name, v, self.get_default(ori_name)))
            if 'req' in k:
                self._req = Node(None, k, v)
                self._req.type = upper_name + "Req"
                self.__merge_default(self._req, 'req')
                # self._record_property(self._req)
            elif 'resp' in k:
                self._resp = Node(None, k, v)
                self._resp.type = upper_name + "Resp"
                self.__merge_default(self._resp, 'resp')
                # self._record_property(self._resp)
            elif 'url_param' in k:
                self._url_param = Node(None, k, v)
                self._url_param.type = upper_name + "UrlParam"
                self.__merge_default(self._url_param, 'url_param')
            elif 'context' in k:
                self._context = Node(None, k, v)
                self._context.type = upper_name + "Context"
                self.__merge_default(self._context, 'context')
            elif 'cookie' in k:
                self._cookie = Node(None, k, v)
                self._cookie.type = upper_name + "Cookie"
                self.__merge_default(self._cookie, 'cookie')
            elif 'url' == k:
                self._url = v
            elif 'method' == k:
                self._method = v
            elif 'api_tags' == k:
                if not isinstance(v, list):
                    v = [v]
                self._api_tags = v
            elif 'doc_tags' == k:
                if not isinstance(v, list):
                    v = [v]
                self._doc_tags = v
            elif 'url_gw_prefix' == k:
                self._url_gw_prefix = v
            elif 'url_prefix' == k:
                self._url_prefix = v
            elif 'url_suffix' == k:
                self._url_suffix = v
            elif 'note' == k:
                self._note = v
            elif 'opposite' == k:
                assert isinstance(v, bool)
                self._opposite = v
            elif 'no_resp' == k:
                assert isinstance(v, bool)
                self._no_resp = v
            elif 'command_code' == k:
                self._command_code = v
            else:
                print("不支持的节点类型[%s]" % k)

        if not self._method:
            self._method = tool.get_map_value(self._default_map, 'method', 'POST')

        if not self._url_prefix:
            self._url_prefix = tool.get_map_value(self._default_map, 'url_prefix', '')

        if not self._gw_url_prefix:
            self._gw_url_prefix = tool.get_map_value(self._default_map, 'url_gw_prefix', '')

        if not self._url_suffix:
            self._url_suffix = self._name

        if not self._url_path:
            self._url_path = tool.url_concat(self._url_prefix, self._url_suffix)

        if not self._gw_url_path:
            self._gw_url_path = tool.url_concat(self._gw_url_prefix, self._url_prefix, self._url_suffix)

    @property
    def opposite(self):
        return self._opposite

    @property
    def cookie(self):
        return self._cookie

    @cookie.setter
    def cookie(self, value):
        self._cookie = value

    @property
    def api_tags(self):
        return self._api_tags

    @property
    def doc_tags(self):
        return self._doc_tags

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, ctx):
        self._context = ctx

    @property
    def name(self):
        return self._name

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, v):
        self._method = v

    @property
    def gw_url(self):
        return self._gw_url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, v):
        self._url = v

    @property
    def gw_url_prefix(self):
        return self._gw_url_prefix

    @gw_url_prefix.setter
    def gw_url_prefix(self, v):
        self._gw_url_prefix = v

    @property
    def url_param(self):
        return self._url_param

    @url_param.setter
    def url_param(self, v):
        self._url_param = v

    @property
    def note(self):
        return self._note

    @property
    def req(self):
        return self._req

    @property
    def resp(self):
        return self._resp

    # def __hash__(self):
    #     return hash(self._name)

    def __eq__(self, o):
        return self._name == o._name

    def __str__(self):
        s = "[%s] [%s]\n" % (self.name, self.note)
        return s
