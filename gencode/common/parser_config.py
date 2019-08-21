#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gencode.common import tool
from gencode.common import meta
import util


type_enum = 'ENUM'
type_api = 'API'


def read_enums(json_map):
    for k, v in json_map.items():
        assert tool.contain_dict(v)
        if v['type'].upper() == type_enum:
            if 'note' not in v:
                v['note'] = ""
            meta.Enum.add_enum(tool.make_enum(k, v['note'], v['value']))


def map_to_apis(json_map):
    apis = []
    protocol = json_map['protocol'].upper()
    json_map.pop('protocol')

    if 'url_prefix' in json_map:
        url_prefix = json_map['url_prefix']
        json_map.pop('url_prefix')
    else:
        url_prefix = ""

    read_enums(json_map)

    for k, v in json_map.items():
        if v['type'].upper() == type_enum:
            continue
        # print(k, v, v['type'])
        assert v['type'].upper() == type_api
        if k in [api.name for api in apis]:
            print("api [%s] already existed" % (k))
            assert False
        req = v['req']
        resp = v['resp']

        # req
        if 'name' not in req:
            req['name'] = util.gen_lower_camel(k) + "Req"
        if 'type' not in req:
            req['type'] = util.gen_upper_camel(k) + "Req"
        if 'note' not in req:
            req['note'] = ""
        req = meta.Node(req['name'], True, req['note'], req['type'], req['fields'], True)

        # resp
        if 'name' not in resp:
            resp['name'] = util.gen_lower_camel(k) + "Resp"
        if 'type' not in resp:
            resp['type'] = util.gen_upper_camel(k) + "Resp"
        if 'note' not in resp:
            resp['note'] = ""
        resp = meta.Node(resp['name'], True, resp['note'], resp['type'], resp['fields'], False)

        # url
        if 'note' not in v:
            v['note'] = ""
        if 'url' not in v:
            v['url'] = "%s/%s" % (url_prefix, util.gen_underline_name(k))

        # url_param
        if protocol == meta.proto_http:
            if 'url_param' not in v:
                v['url_param'] = {}
            url_param = v['url_param']
            if 'type' not in url_param:
                url_param['type'] = util.gen_upper_camel(k) + "UrlParam"
            if 'note' not in url_param:
                url_param['note'] = ""
            if 'name' not in url_param:
                url_param['name'] = util.gen_lower_camel(k) + "UrlParam"
            if 'fields' not in url_param:
                url_param['fields'] = {}
            for field_name, field_value in url_param['fields'].items():
                print("fields:", field_name, field_value)
                assert not tool.contain_dict(field_value)
            url_param = meta.Node(url_param['name'], True, url_param['note'], url_param['type'], url_param['fields'], True)
        else:
            url_param = None

        # api
        if 'method' not in v:
            v['method'] = 'POST'
        api = meta.Api(k, req, resp, v['note'])
        api.url = v['url']
        api.method = v['method']
        api.url_param = url_param
        apis.append(api)
    return apis, protocol


def gen_apis(filename):
    json_map = util.readjson(filename)
    return map_to_apis(json_map)
