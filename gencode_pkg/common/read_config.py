#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
from gencode_pkg.common import data_type
# from util import add_struct
# import test_case
from gencode_pkg.common import util


def list_to_interface(field_name, field_value, struct_info, all_type):
    assert type(field_value) == list
    for l in field_value:
        st, obj = struct_info.add_attribute(field_name, l, True)
        if obj:
            kv_to_interface(field_name, l, st, all_type)
        elif type(l) == list:
            print("list in list")
            assert False
            list_to_interface(field_name, l, struct_info, all_type)


def kv_to_interface(field_name, field_value, struct_info, all_type):
    if type(field_value) in (dict, OrderedDict):
        util.add_struct(all_type, struct_info)
        for k, v in field_value.items():
            st, obj = struct_info.add_attribute(k, v, False)
            if obj:
                kv_to_interface(k, v, st, all_type)

    elif type(field_value) == list:
        # if field_name.index("userInfos") != -1:
        #    pass
            # import pdb
            # pdb.set_trace()
        list_to_interface(field_name, field_value, struct_info, all_type)


def gen_enum(enum_type, enum_comment, enum_values, to_enums):
    enum = data_type.Enum(enum_type, enum_comment)
    for enum_value in enum_values:
        params = enum_value.split("|", -1)
        value = params[0]
        comment = ""
        if len(params) > 1:
            comment = params[1]
        enum.add_value(data_type.EnumValue(value, comment))
    util.add_enum(to_enums, enum)


def map_to_interface(json_map):
    interfaces = []
    for interface_name, interface_value in json_map.items():
        if data_type.InterfaceInfo(interface_name) in interfaces:
            print("interface [%s] already existed" % (interface_name))
            assert False
        strs = interface_name.split('|', -1)
        interface_name = strs[0]
        comment = None
        interface = data_type.InterfaceInfo(interface_name)

        if len(strs) > 1:
            comment = strs[1]
        interface.comment = comment
        if len(strs) > 2:
            interface._type = strs[2]
            if interface._type.upper() == 'ENUM':
                gen_enum(interface_name, comment, interface_value, interface.get_enums())
                continue

        util.add_interface(interfaces, interface)
        print(interface_value)
        for struct_name, struct_value in interface_value.items():
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
                interface.req_st = data_type.StructInfo(struct_name, struct_comment, True, False)
                kv_to_interface(struct_name, struct_value, interface.req_st, interface.get_types())
                print("reqname:", interface.req_st.get_name())
            elif struct_type == 'resp':
                interface.resp_st = data_type.StructInfo(struct_name, struct_comment, False, True)
                kv_to_interface(struct_name, struct_value, interface.resp_st, interface.get_types())
                print("respname:", interface.resp_st.get_name())
            else:
                print("类型不明:", interface_name, struct_name)
                assert False

    return interfaces


def gen_request_response(filename):
    json_map = util.readjson(filename)
    return map_to_interface(json_map)
    # test_case.gen_test_case(filename)


interfaces = gen_request_response("../../json/newVersion.json")
for interface in interfaces:
    print(interface.get_req().to_json())
    print(interface.get_resp().to_json())
# gen_request_response("/home/ubuntu/gencode/json/newVersion2.json")
