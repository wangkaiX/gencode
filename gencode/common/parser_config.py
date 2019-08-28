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
        meta.Enum.add_enum(tool.make_enum(k, v['note'], v['value']))


def parser_protocol(protocol_map):
    protocol = meta.Protocol(protocol_map['type'].upper())
    if 'method' in protocol_map:
        protocol.method = protocol_map['method']
    if 'url_prefix' in protocol_map:
        protocol.url_prefix = protocol_map['url_prefix']
    if 'url' in protocol_map:
        protocol.url_prefix = protocol_map['url']
    return protocol


def gen_req(api_name, api_map, default_req):
    if 'req' not in api_map:
        api_map['req'] = {}
    req = {**default_req, **api_map['req']}

    if 'name' not in req:
        req['name'] = util.gen_lower_camel(api_name) + "Req"
    if 'type' not in req:
        req['type'] = util.gen_upper_camel(api_name) + "Req"
    if 'note' not in req:
        req['note'] = ""
    if 'fields' not in req:
        req['fields'] = {}

    return meta.Node(req['name'], True, req['note'], req['type'], req['fields'], 'req')


def gen_resp(api_name, api_map, default_resp):
    if 'resp' not in api_map:
        api_map['resp'] = {}
    resp = {**default_resp, **api_map['resp']}

    if 'name' not in resp:
        resp['name'] = util.gen_lower_camel(api_name) + "Resp"
    if 'type' not in resp:
        resp['type'] = util.gen_upper_camel(api_name) + "Resp"
    if 'note' not in resp:
        resp['note'] = ""
    if 'fields' not in resp:
        resp['fields'] = {}

    return meta.Node(resp['name'], True, resp['note'], resp['type'], resp['fields'], 'resp')


def gen_context(api_name, api_map, default_context):
    if 'context' not in api_map:
        api_map['context'] = {}
    context = {**default_context, **api_map['context']}

    # context
    if 'name' not in context:
        context['name'] = util.gen_lower_camel(api_name) + "Context"
    if 'type' not in context:
        context['type'] = util.gen_upper_camel(api_name) + "Context"
    if 'note' not in context:
        context['note'] = ""
    if 'fields' not in context:
        context['fields'] = {}
    return meta.Node(context['name'], True, context['note'], context['type'], context['fields'], 'context')


def gen_url_param(api_name, api_map, default_url_param):
    if 'url_param' not in api_map:
        api_map['url_param'] = {}
    url_param = {**default_url_param, **api_map['url_param']}

    if 'type' not in url_param:
        url_param['type'] = util.gen_upper_camel(api_name) + "UrlParam"
    if 'note' not in url_param:
        url_param['note'] = ""
    if 'name' not in url_param:
        url_param['name'] = util.gen_lower_camel(api_name) + "UrlParam"
    if 'fields' not in url_param:
        url_param['fields'] = {}
    for field_name, field_value in url_param['fields'].items():
        print("fields:", field_name, field_value)
        assert not tool.contain_dict(field_value)
    return meta.Node(url_param['name'], True, url_param['note'], url_param['type'], url_param['fields'], 'url_param')


def get_default(default_map, name):
    if name not in default_map:
        default_map[name] = {}
    return default_map[name]


def parser_node(apis_map, protocol):
    apis = []

    default_map = get_default(apis_map, 'default')

    default_context = get_default(default_map, 'context')
    default_req = get_default(default_map, 'req')
    default_resp = get_default(default_map, 'resp')
    default_url_param = get_default(default_map, 'url_param')
    url_prefix = get_default(default_map, "url_prefix")

    for k, v in apis_map.items():
        if k in [api.name for api in apis]:
            print("api [%s] already existed" % (k))
            assert False

        req = gen_req(k, v, default_req)
        resp = gen_resp(k, v, default_resp)
        context = gen_context(k, v, default_context)
        url_param = gen_url_param(k, v, default_url_param)

        # url
        if 'note' not in v:
            v['note'] = ""
        if 'url' not in v:
            v['url'] = "%s/%s" % (url_prefix, util.gen_underline_name(k))

        # method
        if 'method' not in v:
            if protocol.type == meta.proto_http:
                v['method'] = 'POST'
            elif protocol.type == meta.proto_graphql:
                v['method'] = 'query'

        # api
        api = meta.Api(k, req, resp, v['note'])
        api.url = v['url']
        api.method = v['method']
        api.url_param = url_param
        api.context = context
        apis.append(api)
    return apis


def parser_config(config_map, protocol):
    configs = []
    for k, v in config_map.items():
        name, required, note, _type = tool.split_ori_name(k)
        config = meta.Node(name, required, note, _type, v, 'config')
        configs.append(config)
    return configs


def map_to_apis(json_map):
    parser_enum(json_map['enum'])
    protocol = parser_protocol(json_map['protocol'])
    if 'config' in json_map:
        configs = parser_config(json_map['config'], protocol)
        config_map = json_map['config']
    else:
        configs = []
        config_map = {}
    apis = parser_node(json_map['api'], protocol)
    return apis, protocol, configs, config_map


def gen_apis(filename):
    json_map = util.readjson(filename)
    return map_to_apis(json_map)
