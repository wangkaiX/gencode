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
    protocol = json_map['protocol']
    json_map.pop('protocol')

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
        # print("k:", k)
        if 'name' not in req:
            req['name'] = util.gen_lower_camel(k) + "Req"
        if 'type' not in req:
            req['type'] = util.gen_upper_camel(k) + "Req"
        if 'note' not in req:
            req['note'] = ""
        req = meta.Node(req['name'], True, req['note'], req['type'], req['fields'], True)
        if 'name' not in resp:
            resp['name'] = util.gen_lower_camel(k) + "Resp"
        if 'type' not in resp:
            resp['type'] = util.gen_upper_camel(k) + "Resp"
        if 'note' not in resp:
            resp['note'] = ""
        resp = meta.Node(resp['name'], True, resp['note'], resp['type'], resp['fields'], False)
        if 'note' not in v:
            v['note'] = ""
        apis.append(meta.Api(k, req, resp, v['note']))
    return apis, protocol


def gen_apis(filename):
    json_map = util.readjson(filename)
    return map_to_apis(json_map)


'''
apis = gen_apis("../../json/newVersion3.json")
with open("result.txt", "w") as f:
    meta.Type = meta.TypeGraphql
    for api in apis:
        f.write(str(api) + "\n")
    meta.Type = meta.TypeProto
    for api in apis:
        f.write(str(api) + "\n")
'''
