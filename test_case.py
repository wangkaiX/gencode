#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


def gen_test_case(file_name):
    # print("filename:", file_name)
    file = open(file_name, "r")
    json_map = json.loads(file.read())
    (res, vres), (resp, vresp) = json_map.items()
    print(res, vres)
    print(resp, vresp)
    json_str = json.dumps(json_map, separators=(',', ':'), indent=4)
    beg = 0
    rdquote_index = json_str.find('":', beg)
    while rdquote_index != -1:
        ldquote_index = json_str.rfind('"', 0, rdquote_index)
        assert ldquote_index != -1
        key_end_index = json_str.find('|', ldquote_index, rdquote_index)
        if key_end_index == -1:
            key_end_index = rdquote_index
        json_str = json_str[:key_end_index] + json_str[rdquote_index:]
        rdquote_index = json_str.find('":', key_end_index + 2)
    test_file_name = file_name.split('.')[0] + "_test.json"
    test_file = open(test_file_name, "w")
    test_file.write(json_str)


gen_test_case("/home/ubuntu/service/interface/create_calculate_job.json")
