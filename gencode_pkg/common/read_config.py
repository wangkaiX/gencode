#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
from gencode_pkg.common import data_type
# from util import add_struct
# import test_case
from gencode_pkg.common import util


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


def read_enum(json_map, all_enum):
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
                gen_enum(interface_name, comment, interface_value, all_enum)


def map_to_interface(json_map, all_enum):
    read_enum(json_map, all_enum)
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
                continue

        util.add_interface(interfaces, interface)
        for struct_name, struct_value in interface_value.items():
            strs = struct_name.split('|', -1)
            if (len(strs) < 2):
                print(struct_name, "未指定类型")
                assert False
            struct_name = strs[0]
            struct_type = strs[1]
            struct_comment = None
            if len(strs) > 2:
                struct_comment = strs[2]
            if struct_type == 'req':
                if not interface.req_url_param_st:
                    interface.req_url_param_st = data_type.StructInfo(struct_name, struct_comment, data_type.st_type.req)
                kv_to_interface(struct_name, struct_value, interface.req_url_param_st, interface.get_types(), all_enum)

                interface.req_st = data_type.StructInfo(struct_name, struct_comment, data_type.st_type.req)
                interface.req_url_param_st.set_name(interface.req_st.get_name())
                interface.req_url_param_st.set_comment(interface.req_st.get_comment())

                kv_to_interface(struct_name, struct_value, interface.req_st, interface.get_types(), all_enum)
            elif struct_type == 'resp':
                interface.resp_st = data_type.StructInfo(struct_name, struct_comment, data_type.st_type.resp)
                kv_to_interface(struct_name, struct_value, interface.resp_st, interface.get_types(), all_enum)
            elif struct_type == 'url':
                interface.url = struct_value
            elif struct_type == 'urlparam':
                if not interface.req_url_param_st:
                    interface.req_url_param_st = data_type.StructInfo(struct_name, struct_comment, data_type.st_type.req)
                kv_to_interface(struct_name, struct_value, interface.req_url_param_st, interface.get_types(), all_enum)
                print(interface_name + util.gen_title_name(struct_name))

                interface.url_param_st = data_type.StructInfo(
                        interface_name + util.gen_title_name(struct_name),
                        struct_comment,
                        data_type.st_type.url_param)
                kv_to_interface(struct_name, struct_value, interface.url_param_st, interface.get_types(), all_enum)
            else:
                print("类型不明inetrface:[%s]st_name:[%s]st_type[%s]:" % (interface_name, struct_name, struct_type))
                assert False

    return interfaces


def gen_request_response(filename, all_enum):
    json_map = util.readjson(filename)
    return map_to_interface(json_map, all_enum)
    # test_case.gen_test_case(filename)


# interfaces = gen_request_response("../../json/newVersion.json", [])
# with open("json.txt", "w") as f:
#     for interface in interfaces:
#         print(interface.get_req().to_json(), interface.get_req().get_null_count())
#         f.write(interface.get_req().to_json_without_i(range(0, interface.get_req().get_null_count()), True, True))
#         for i in range(0, interface.get_req().get_null_count()):
#             f.write(interface.get_req().to_json_without_i([i], True, True))
# gen_request_response("/home/ubuntu/gencode/json/newVersion2.json")
