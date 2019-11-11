#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.common import tool


class EnumValue:
    def __init__(self, value):
        rets = tool.split(value, '|', 2)
        self.value = rets[0]
        self.note = rets[1]

    def __eq__(self, o):
        return self.value == o.value


class Enum:
    def __init__(self, name, value_map):
        self.__name = name
        self.__values = []
        for value in value_map['value']:
            enum_value = EnumValue(value)
            if enum_value in self.__values:
                print("有重复的枚举值[%s]", enum_value)
                assert False
            self.__values.append(EnumValue(value))
        self.__note = value_map['note']

    @property
    def name(self):
        return self.__name

    @property
    def note(self):
        return self.__note

    @property
    def values(self):
        return self.__values
