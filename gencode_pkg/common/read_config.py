#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
from gencode_pkg.common import data_type
# from util import add_struct
# import test_case
from gencode_pkg.common import util


def list_to_interface(field_name, field_value, struct_info):
    assert type(field_value) == list
    for l in field_value:
        if type(l) in (dict, OrderedDict):
            struct_info.set_list(True)
            kv_to_interface(field_name, l, struct_info)
        elif type(l) == list:
            list_to_interface(field_name, l, struct_info)
        else:
            struct_info.add_attribute(field_name, field_value)
            break


def kv_to_interface(field_name, field_value, struct_info):
    if type(field_value) in (dict, OrderedDict):
        # field_name, necessary, comment, type_kind, type_type = data_type.get_key_attr(field_name, field_value)
        # util.add_struct(to_dict, base_type.get_name())

        for k, v in field_value.items():
            struct_info.add_attribute(k, v)
            if len(struct_info.member_classs()) > 0:
                kv_to_interface(k, v, struct_info.member_classs()[-1])

    elif type(field_value) == list:
        list_to_interface(field_name, field_value, struct_info)


def map_to_interface(json_map):
    interfaces = {}
    for interface_name, interface_info in json_map.items():
        if interface_name in interfaces.keys():
            print("interface [%s] already existed" % (interface_name))
            assert False
        strs = interface_name.split('|', -1)
        interface_name = strs[0]
        comment = None
        interfaces[interface_name] = data_type.InterfaceInfo()
        if len(strs) > 1:
            comment = strs[1]
        interfaces[interface_name].comment = comment

        print(interface_info)
        for struct_name, struct_info in interface_info.items():
            # print(json_map)
            # print(interface_name)
            # print(struct_name)
            # print(struct_info)
            strs = struct_name.split('|', -1)
            struct_name = strs[0]
            struct_type = strs[1]
            struct_comment = None
            if len(strs) > 2:
                struct_comment = strs[2]
            if struct_type == 'req':
                interfaces[interface_name].req_st = data_type.StructInfo(struct_name, struct_comment, True, False)
                kv_to_interface(struct_name, struct_info, interfaces[interface_name].req_st)
                print("reqname:", interfaces[interface_name].req_st.get_name())
            elif struct_type == 'resp':
                interfaces[interface_name].resp_st = data_type.StructInfo(struct_name, struct_comment, False, True)
                kv_to_interface(struct_name, struct_info, interfaces[interface_name].resp_st)
                print("respname:", interfaces[interface_name].resp_st.get_name())
            else:
                print("类型不明:", interface_name, struct_name)
                assert False

    return interfaces


def gen_request_response(filename):
    json_map = util.readjson(filename)
    return map_to_interface(json_map)
    # test_case.gen_test_case(filename)


res = gen_request_response("../../json/newVersion.json")
for k, v in res.items():
    print(k, v)
# gen_request_response("/home/ubuntu/gencode/json/newVersion2.json")
