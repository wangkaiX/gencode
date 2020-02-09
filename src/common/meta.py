#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.common import tool
from src.common import enum_type
from src.common import field_type
import util.python.util as util
from src.go.gin import gin as go_gin
import copy


class Protocol:
    def __init__(self, tree_map):
        self.__framework_type = None
        self.__apis = []
        self.__config = None
        self.__default_map = None
        self.__enums = []
        self.__imports = []
        self.__nodes = []
        self.__node_map = {}
        # tree_map = parser.Json5(filename=filename).parser()

        self.__method = None

        # parser
        self.__parser(tree_map)

    @property
    def framework_type(self):
        return self.__framework_type

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
        if self.__framework_type == field_type.go_gin:
            gencode = go_gin.GoGin(self, **kwargs)
            gencode.gen_code()
        else:
            print("暂不支持")
            assert False

    def __parser(self, tree_map):
        self.__parser_protocol(tree_map['protocol'])
        # self.__parser_import(tree_map['import'])
        self.__parser_default(tree_map['default'])
        self.__parser_enum(tree_map['enum'])
        self.__parser_config('config', tree_map)
        self.__parser_api(tree_map['api'])
        self.__parser_all_api_nodes()

    def __parser_all_api_nodes(self):
        nodes = []
        for api in self.apis:
            nodes += [api.req, api.resp, api.context, api.url_param, api.cookie]
        self.__nodes = tool.get_all_nodes(nodes)

    def __parser_protocol(self, protocol_map):
        self.__framework_type = protocol_map['framework_type']
        tool.assert_framework_type(self.__framework_type)
        if self.__framework_type == field_type.graphql:
            self.__parser_go_graphql(protocol_map)
        elif self.__framework_type == field_type.grpc:
            self.__parser_go_grpc(protocol_map)
        elif self.__framework_type == field_type.go_gin:
            self.__parser_go_gin(protocol_map)

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

    @property
    def config(self):
        return self.__config

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
        upper_name = util.gen_upper_camel(self.name)
        self.__req = Node(None, upper_name + "Req", self.get_default('req'))
        self.__resp = Node(None, upper_name + "Resp", self.get_default('resp'))
        self.__url_param = Node(None, upper_name + "UrlParam", self.get_default('url_param'))
        self.__context = Node(None, upper_name + "Context", self.get_default('context'))
        self.__cookie = Node(None, upper_name + "Cookie", self.get_default('cookie'))

        self.__url = None
        self.__gw_url = None
        self.__url_gw_prefix = None
        self.__url_suffix = None
        self.__url_prefix = None
        self.__method = None

        # 接口对内对外
        self.__api_tags = None
        # 文档类别(前端，后台)
        self.__doc_tags = None

        # parser
        self.__parser()

    def get_default(self, name, default_value={}):
        if name not in self.__default_map.keys():
            return default_value
        return self.__default_map[name]

    @property
    def has_file(self):
        return self.__req.has_file

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

        if not self.__url_gw_prefix:
            self.__url_gw_prefix = tool.get_map_value(self.__default_map, 'url_gw_prefix', '')

        if not self.__url_suffix:
            self.__url_suffix = self.__name

        if not self.__url:
            self.__url = tool.url_concat(self.__url_prefix, self.__url_suffix)

        if not self.__gw_url:
            self.__gw_url = tool.url_concat(self.url_gw_prefix, self.__url_prefix, self.__url_suffix)

    @property
    def cookie(self):
        return self.__cookie

    @cookie.setter
    def cookie(self, value):
        self.__cookie = value

    @property
    def api_tags(self):
        if self.__api_tags:
            return self.__api_tags
        return []

    @api_tags.setter
    def api_tags(self, value):
        self.__api_tags = value

    @property
    def doc_tags(self):
        if self.__doc_tags:
            return self.__doc_tags
        return []

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
    def url_gw_prefix(self):
        return self.__url_gw_prefix

    @url_gw_prefix.setter
    def url_gw_prefix(self, v):
        self.__url_gw_prefix = v

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


class Member:
    def __init__(self, parent, name, value_map):
        self.__name, self.__required, self.__note, self.__type = tool.split_ori_name(name)
        if parent:
            self.__full_path = parent.full_path + [self.__name]
        else:
            self.__full_path = [self.__name]
        self.__grpc_index = None
        self.__parent = parent
        self.__value_map = value_map
        self.__dimension = tool.get_dimension(value_map)
        if self.__type:
            self.type = self.__type

        if not self.__note:
            self.__note = self.__name

    @property
    def full_path(self):
        return self.__full_path

    @property
    def grpc_index(self):
        assert self.__grpc_index is not None
        return self.__grpc_index

    @grpc_index.setter
    def grpc_index(self, value):
        assert isinstance(value, int)
        self.__grpc_index = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def required(self):
        return self.__required

    @property
    def note(self):
        return self.__note

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, t):
        assert not isinstance(t, field_type.FieldType)
        self.__type = field_type.FieldType(t)

    @property
    def value_map(self):
        return self.__value_map

    @value_map.setter
    def value_map(self, v):
        self.__value_map = v

    @property
    def dimension(self):
        return self.__dimension


class Field(Member):
    def __init__(self, father, name, value_map):
        Member.__init__(self, father, name, value_map)
        if not self.type:
            self.type = util.get_base_type(value_map)

    def __eq__(self, o):
        return self.name == o.name

    @property
    def value(self):
        return self.value_map

    def __str__(self):
        s = "[%s] [%s] [%s] [%s] [%s] [dim:%s]\n" % \
                (self.name, self.required, self.note, self.type, self.value_map, self.dimension)
        return s


'''
class Attr:
    __type_list = ('req', 'resp', 'enum', 'api', 'config', 'url_param', 'context', 'cookie')

    def __init__(self, _type):
        if _type not in Attr.__type_list:
            print(_type)
            assert False
        self.__type = _type

    def __getattr__(self, name):
        assert 'is_' == name[:3] and name[3:] in Attr.__type_list
        return name == ('is_' + self.__type)
'''


class Node(Member):
    def __init__(self, parent, name, value_map):
        if not value_map:
            value_map = {}
        Member.__init__(self, parent, name, value_map)
        assert tool.contain_dict(value_map)
        if not self.type:
            self.type = util.gen_upper_camel(self.name)

        self.__curr_child_index = 1
        self.__nodes = []
        self.__fields = []
        self.__has_time = False
        self.__has_file = False

        self.parser_children()
        self.value_map = tool.dict_key_clean(self.value_map)
        for member in self.fields + self.nodes:
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
        member.grpc_index = self.__curr_child_index
        if isinstance(member, Node):
            self.add_node(member)
        elif isinstance(member, Field):
            self.add_field(member)
        else:
            print("Unknown Type:", member)
            assert False
        self.__curr_child_index += 1
        # print(member.type, type(member.type), type(member))
        if not self.__has_file and member.type.is_file:
            self.__has_file = True
        if not self.__has_time and member.type.is_time:
            self.__has_time = True

    def add_node(self, node):
        if node.name not in [n.name for n in self.nodes]:
            self.nodes.append(node)
        else:
            print("重复的字段名:", node.name)
            assert False

    def add_field(self, field):
        if field not in self.fields:
            self.fields.append(field)
        else:
            print("重复的字段名:", field.name)
            assert False

    def parser_children(self):
        value = tool.get_value(self.value_map)
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
            (self.name, self.required, self.note, self.type, self.value_map, self.dimension)
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
