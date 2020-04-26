#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from code_framework.common import tool


class EnumValue:
    def __init__(self, value):
        rets = tool.split(value, '|', 2)
        self.value = rets[0]
        self.note = rets[1]

    def __eq__(self, o):
        return self.value == o.value

    def __str__(self):
        return "[%s:%s]" % (self.value, self.note)


class Enum:
    def __init__(self, name, value_map):
        self.__name = name
        self.__name, self.__base_type = tool.split(self.__name, "|", 2)
        self.__values = []
        for value in value_map['value']:
            enum_value = EnumValue(value)
            if enum_value in self.__values:
                print("有重复的枚举值[%s]", enum_value)
                assert False
            self.__values.append(enum_value)
        # 必须要有注释
        self.__note = value_map['note']

    @property
    def base_type(self):
        return self.__base_type

    @property
    def name(self):
        return self.__name

    @property
    def note(self):
        return self.__note

    @property
    def values(self):
        return self.__values

    def __eq__(self, o):
        return self.name == o.name

    def __expr__(self):
        return str(self)

    def __str__(self):
        values = ""
        for value in self.values:
            values += str(value)
        return "%s:%s" % (self.name, values)
