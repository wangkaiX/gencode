#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


def gen_test_case(file_name):
    ifile = open(file_name, "r")
    json_map = json.loads(ifile.read(), encoding='utf8')
    (res, vres), (resp, vresp) = json_map.items()
    json_str = json.dumps(json_map, separators=(',', ':'), indent=4, ensure_ascii=False)
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
    index = file_name.find(".json")
    test_file_name = file_name[:index] + "_test.json"
    test_file = open(test_file_name, "w", encoding='utf8')
    test_file.write(json_str)
    test_file.close()


# gen_test_case("/home/ubuntu/service/interface/create_project.json")
