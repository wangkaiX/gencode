#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gencode.common import tool
from gencode.common import meta
import util.python.util as util
from abc import abstractmethod
import json5


type_enum = 'ENUM'
type_api = 'API'


def parser_enum(enum_map):
    enums = []
    for k, v in enum_map.items():
        assert tool.contain_dict(v)
        if 'note' not in v:
            v['note'] = ""
        enum = tool.make_enum(k, v['note'], v['value'])
        if 'option' not in v:
            v['option'] = ""
        enum.option = v['option']
        assert tool.append_member(enums, enum)


def parser_protocol(protocol_map):
    protocol = meta.Protocol(protocol_map['type'].upper())
    if 'method' in protocol_map:
        protocol.method = protocol_map['method']
    if 'url_prefix' in protocol_map:
        protocol.url_prefix = protocol_map['url_prefix']
    if 'url' in protocol_map:
        protocol.url_prefix = protocol_map['url']
    return protocol


def get_default(default_map, name, default_value=None):
    if name not in default_map:
        default_map[name] = default_value
    return default_map[name]


def get_value(json_map, name, default_value):
    if name not in json_map:
        json_map[name] = default_value
    return json_map[name]


def gen_node(api_name, api_map, default_map, node_name):
    default_fields = get_default(default_map, node_name)
    if node_name not in api_map:
        api_map[node_name] = {}
    node_map = api_map[node_name]
    if 'name' not in node_map:
        node_map['name'] = util.gen_lower_camel(api_name) + util.gen_upper_camel(node_name)
    if 'type' not in node_map:
        node_map['type'] = util.gen_upper_camel(api_name) + util.gen_upper_camel(node_name)
    if 'note' not in node_map:
        node_map['note'] = ''
    if 'fields' not in node_map:
        node_map['fields'] = {}
    assert isinstance(node_map, dict)
    node_map['fields'] = {**node_map['fields'], **default_fields}

    return meta.Node(node_map['name'], True, node_map['note'], node_map['type'], node_map['fields'], node_name, '')


def parser_node(apis_map, default_map, protocol):
    apis = []

    url_prefix = get_default(default_map, "url_prefix", "")
    gw_url_prefix = get_default(default_map, "gw_url_prefix", "")
    default_http_method = get_default(default_map, "http_method", "POST")
    default_graphql_method = get_default(default_map, "graphql_method", "query")
    default_api_tag = get_default(default_map, "api_tag", "")
    default_doc_tag = get_default(default_map, "doc_tag", "")

    for k, v in apis_map.items():
        if k in [api.name for api in apis]:
            print("api [%s] already existed" % (k))
            assert False

        # url
        # if 'note' not in v:
        #     v['note'] = ""
        if 'url' not in v:
            if protocol.type == meta.proto_http:
                v['url'] = "%s/%s" % (url_prefix, util.gen_underline_name(k))
            elif protocol.type == meta.proto_grpc:
                v['url'] = "%s/%s/%s" % (url_prefix, util.gen_upper_camel(k), util.gen_upper_camel(k)) + "Req"

        # gw_url
        if 'gw_url' not in v:
            if protocol.type == meta.proto_http:
                v['gw_url'] = "%s%s" % (gw_url_prefix, v['url'])
            elif protocol.type == meta.proto_grpc:
                v['gw_url'] = "%s%s" % (gw_url_prefix, v['url'])

        # method
        if 'method' not in v:
            if protocol.type == meta.proto_http:
                v['method'] = default_http_method
            elif protocol.type == meta.proto_graphql:
                v['method'] = default_graphql_method
            elif protocol.type == meta.proto_grpc:
                v['method'] = 'POST'
            else:
                assert False

        # tag
        v['api_tag'] = get_value(v, 'api_tag', default_api_tag)
        v['doc_tag'] = get_value(v, 'doc_tag', default_doc_tag)

        req = gen_node(k, v, default_map, 'req')
        resp = gen_node(k, v, default_map, 'resp')
        context = gen_node(k, v, default_map, 'context')
        url_param = gen_node(k, v, default_map, 'url_param')
        cookie = gen_node(k, v, default_map, 'cookie')

        # api
        api = meta.Api(k, req, resp, v['note'])
        api.gw_url = v['gw_url']
        api.url = v['url']
        api.method = v['method']
        api.url_param = url_param
        api.context = context
        api.api_tag = v['api_tag'].upper()
        api.doc_tag = v['doc_tag']
        api.cookie = cookie
        apis.append(api)
    return apis


def parser_config(config_map, protocol):
    configs = []
    for k, v in config_map.items():
        name, required, note, _type = tool.split_ori_name(k)
        config = meta.Node(name, required, note, _type, v, 'config', '')
        configs.append(config)
    return configs


def map_to_apis(json_map):
    default_enum = get_default(json_map, 'enum')
    parser_enum(default_enum)
    protocol = parser_protocol(json_map['protocol'])

    default_map = get_default(json_map, 'default')

    if 'config' in json_map:
        configs = parser_config(json_map['config'], protocol)
        config_map = json_map['config']
    else:
        configs = []
        config_map = {}
    apis = parser_node(json_map['api'], default_map, protocol)
    return apis, protocol, configs, config_map


def gen_apis(filename):
    json_map = util.readjson(filename)
    return map_to_apis(json_map)


class Parser:
    def __init__(self, filename, fp, text):
        if (int(bool(filename)) + int(bool(fp)) + int(bool(text))) != 1:
            print("参数有误", filename, fp, text)
            assert False
        self.filename = filename
        self.fp = fp
        self.text = text
        print("base parser")

    def parser(self):
        if self.filename:
            self.parser_file()
        elif self.fp:
            self.parser_fp()
        return self.parser_text()

    def parser_file(self):
        self.fp = open(self.filename, "rb")
        self.parser_fp()

    def parser_fp(self):
        self.text = self.fp.read()
        self.parser_text()

    @abstractmethod
    def parser_text(self):
        assert False

    def parser_dict(self):
        assert False


class Json5(Parser):
    def __init__(self, filename, fp, text):
        Parser.__init__(self, filename, fp, text)

    def parser_text(self):
        return json5.loads(self.text)
