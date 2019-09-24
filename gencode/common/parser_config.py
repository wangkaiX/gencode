#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gencode.common import tool
from gencode.common import meta
import util


type_enum = 'ENUM'
type_api = 'API'


def parser_enum(enum_map):
    for k, v in enum_map.items():
        assert tool.contain_dict(v)
        if 'note' not in v:
            v['note'] = ""
        enum = tool.make_enum(k, v['note'], v['value'])
        if 'option' not in v:
            v['option'] = ""
        enum.option = v['option']
        meta.Enum.add_enum(enum)


def parser_protocol(protocol_map):
    protocol = meta.Protocol(protocol_map['type'].upper())
    if 'method' in protocol_map:
        protocol.method = protocol_map['method']
    if 'url_prefix' in protocol_map:
        protocol.url_prefix = protocol_map['url_prefix']
    if 'url' in protocol_map:
        protocol.url_prefix = protocol_map['url']
    return protocol


'''
def gen_req(api_name, api_map, default_req):
    if 'req' not in api_map:
        api_map['req'] = {}
    req = api_map['req']

    if 'name' not in req:
        req['name'] = util.gen_lower_camel(api_name) + "Req"
    if 'type' not in req:
        req['type'] = util.gen_upper_camel(api_name) + "Req"
    if 'note' not in req:
        req['note'] = ""
    if 'fields' not in req:
        req['fields'] = {}
    assert isinstance(req['fields'], dict)
    req['fields'] = {**req['fields'], **default_req}

    return meta.Node(req['name'], True, req['note'], req['type'], req['fields'], 'req', '')


def gen_resp(api_name, api_map, default_resp):
    if 'resp' not in api_map:
        api_map['resp'] = {}
    resp = api_map['resp']

    if 'name' not in resp:
        resp['name'] = util.gen_lower_camel(api_name) + "Resp"
    if 'type' not in resp:
        resp['type'] = util.gen_upper_camel(api_name) + "Resp"
    if 'note' not in resp:
        resp['note'] = ""
    if 'fields' not in resp:
        resp['fields'] = {**default_resp}
    assert isinstance(resp['fields'], dict)
    resp['fields'] = {**resp['fields'], **default_resp}

    return meta.Node(resp['name'], True, resp['note'], resp['type'], resp['fields'], 'resp', '')


def gen_context(api_name, api_map, default_context):
    if 'context' not in api_map:
        api_map['context'] = {}
    context = api_map['context']

    # context
    if 'name' not in context:
        context['name'] = util.gen_lower_camel(api_name) + "Context"
    if 'type' not in context:
        context['type'] = util.gen_upper_camel(api_name) + "Context"
    if 'note' not in context:
        context['note'] = ""
    if 'fields' not in context:
        context['fields'] = {}
    context['fields'] = {**context['fields'], **default_context}

    return meta.Node(context['name'], True, context['note'], context['type'], context['fields'], 'context', '')


def gen_url_param(api_name, api_map, default_url_param):
    if 'url_param' not in api_map:
        api_map['url_param'] = {}
    url_param = api_map['url_param']

    if 'type' not in url_param:
        url_param['type'] = util.gen_upper_camel(api_name) + "UrlParam"
    if 'note' not in url_param:
        url_param['note'] = ""
    if 'name' not in url_param:
        url_param['name'] = util.gen_lower_camel(api_name) + "UrlParam"
    if 'fields' not in url_param:
        url_param['fields'] = {}
    for field_name, field_value in url_param['fields'].items():
        assert not tool.contain_dict(field_value)
    url_param = {**url_param['field'], **default_url_param}
    return meta.Node(url_param['name'], True, url_param['note'], url_param['type'], url_param['fields'], 'url_param', '')
'''


def get_default(default_map, name, default_value={}):
    if name not in default_map:
        default_map[name] = default_value
    return default_map[name]


'''
def gen_cookie(api_name, api_map, default_cookie):
    if 'cookie' not in api_map:
        api_map['cookie'] = {}
    cookie = api_map['cookie']

    # cookie
    if 'name' not in cookie:
        cookie['name'] = util.gen_lower_camel(api_name) + "Cookie"
    if 'type' not in cookie:
        cookie['type'] = util.gen_upper_camel(api_name) + "Cookie"
    if 'note' not in cookie:
        cookie['note'] = ""
    if 'fields' not in cookie:
        cookie['fields'] = {}
    assert isinstance(cookie['fields'], dict)
    cookie['fields'] = {**cookie['fields'], **default_cookie}

    return meta.Node(cookie['name'], True, cookie['note'], cookie['type'], cookie['fields'], 'cookie', '')
'''


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

    '''
    default_context = get_default(default_map, 'context')
    default_req = get_default(default_map, 'req')
    default_resp = get_default(default_map, 'resp')
    default_url_param = get_default(default_map, 'url_param')
    default_cookie = get_default(default_map, 'cookie')
    '''

    url_prefix = get_default(default_map, "url_prefix", "")
    default_http_method = get_default(default_map, "http_method", "POST")
    default_graphql_method = get_default(default_map, "graphql_method", "query")

    for k, v in apis_map.items():
        if k in [api.name for api in apis]:
            print("api [%s] already existed" % (k))
            assert False

        # url
        # if 'note' not in v:
        #     v['note'] = ""
        if 'url' not in v:
            if protocol.type == meta.proto_http:
                v['url'] = "%s/%s" % (url_prefix, k)
            elif protocol.type == meta.proto_grpc:
                v['url'] = "%s/%s/%sReq" % (url_prefix, k, k)

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
        if 'tag' not in v:
            v['tag'] = meta.public

        req = gen_node(k, v, default_map, 'req')
        resp = gen_node(k, v, default_map, 'resp')
        context = gen_node(k, v, default_map, 'context')
        url_param = gen_node(k, v, default_map, 'url_param')
        cookie = gen_node(k, v, default_map, 'cookie')

        # api
        api = meta.Api(k, req, resp, v['note'])
        api.url = v['url']
        api.method = v['method']
        api.url_param = url_param
        api.context = context
        api.tag = v['tag'].upper()
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
