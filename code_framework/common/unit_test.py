#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../..')
from code_framework.common import tool

print(tool.get_map_value({'a': 'b', 'b': 100, 'c': {'d': 300}}, 'a.b', '200'))
print(tool.get_map_value({'a': 'b', 'b': 100, 'c': {'d': 300}}, 'c.d', '200'))

print('*' * 80)
s = tool.distinct_str('///b///', '/')
print(s)
print('*' * 80)

url = tool.url_concat('a', 'b', 'c', '', 'd')
print(url)
url = tool.url_concat('//a//', 'b_dojapfw', 'c', ['x', 'y', '//z//'], 'd')
print(url)
