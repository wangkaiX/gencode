#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gencode.common import tool
from gencode.common import meta
import util


type_enum = 'ENUM'
type_api = 'API'

'''
def list_to_interface(field_name, field_value, struct_info, all_type, all_enum):
    assert type(field_value) == list
    util.add_struct(all_type, struct_info)
    for l in field_value:
        if type(l) == list:
            print("list in list")
            assert False
        if type(l) in (dict, OrderedDict):
            st, obj = struct_info.add_attribute(field_name, l, True, all_enum)
            util.add_struct(all_type, st)
            if obj:
                kv_to_interface(field_name, l, st, all_type, all_enum)
        else:
            struct_info.add_attribute(field_name, field_value, False, all_enum)
            break


def kv_to_interface(field_name, field_value, struct_info, all_type, all_enum):
    util.add_struct(all_type, struct_info)
    if type(field_value) in (dict, OrderedDict):
        for k, v in field_value.items():
            if type(v) == list:
                list_to_interface(k, v, struct_info, all_type, all_enum)
            else:
                st, obj = struct_info.add_attribute(k, v, False, all_enum)
                if obj:
                    util.add_struct(all_type, st)
                    kv_to_interface(k, v, st, all_type, all_enum)

    elif type(field_value) == list:
        list_to_interface(field_name, field_value, struct_info, all_type, all_enum)
'''


def read_enums(json_map):
    for k, v in json_map.items():
        assert tool.contain_dict(v)
        if v['type'].upper() == type_enum:
            meta.Enum.add_enum(tool.make_enum(k, v['note'], v['value']))


def map_to_apis(json_map):
    read_enums(json_map)
    apis = []
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
        print("k:", k)
        req = meta.Node(req['name'], True, req['note'], req['type'], req['fields'], True)
        resp = meta.Node(resp['name'], True, resp['note'], resp['type'], resp['fields'], False)
        apis.append(meta.Api(k, req, resp, v['protocol'], v['note']))
    return apis


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
