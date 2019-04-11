#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
from data_type import get_key_attr
# from util import add_struct
import test_case
import util


def list_to_interface(field_name, from_list, to_dict):
    for l in from_list:
        if type(l) in (dict, OrderedDict):
            map_to_interface(field_name, l, to_dict)
        elif type(l) == list:
            list_to_interface(field_name, l, to_dict)


def map_to_interface(field_name, field_value, to_dict):
    if type(field_value) in (dict, OrderedDict):
        field_name, _, _, _type, _ = get_key_attr(field_name, field_value)
        util.add_struct(to_dict, _type)

        for k, v in field_value.items():
            to_dict[_type].add_attribute(k, v)
            map_to_interface(k, v, to_dict)

    elif type(field_value) == list:
        list_to_interface(field_name, field_value, to_dict)


def gen_request_response(filename):
    json_map = util.readjson(filename)
    (request, v1), (response, v2) = json_map.items()
    request_dict = {}
    map_to_interface(request, v1, request_dict)
    response_dict = {}
    map_to_interface(response, v2, response_dict)
    # for k, v in request_dict.items():
    #     print(k, v)
    # for k, v in response_dict.items():
    #     print(k, v)
    test_case.gen_test_case(filename)
    return request_dict, response_dict


# gen_request_response("/home/ubuntu/service/interface/api.json")
# gen_request_response("/home/ubuntu/service/interface/save_worktable.json")
