#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from code_framework.common import tool


class DataTypeGenerator:
    def __init__(self, nodes, enums, mako_dir):
        self.__nodes = nodes
        self.__enums = enums
        self.__mako_dir = mako_dir
        self.__mako_dir = os.path.join(mako_dir, "cpp")

    def nlohmann_json(self):
        tool.gen_code_file(os.path.join(self.__mako_dir, "nlohmann_json.h"),
                           os.path.join(self.__dir, "types", "types.h"),
                           nodes=self.__nodes,
                           enums=self.__enums,
                           )
        tool.gen_code_file(os.path.join(self.__mako_dir, "nlohmann_json.cpp"),
                           os.path.join(self.__dir, "types", "types.cpp"),
                           nodes=self.__nodes,
                           enums=self.__enums,
                           )

    def rapidjson(self):
        pass

    def protobuf(self):
        pass

    def binary(self):
        pass
