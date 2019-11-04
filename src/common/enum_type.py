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
    def __init__(self, name, note, values=[]):
        self.__name = name
        self.__values = []
        for value in values:
            enum_value = EnumValue(value)
            if enum_value in self.__values:
                print("有重复的枚举值[%s]", enum_value)
                assert False
            self.__values.append(EnumValue(value))
        self.__note = note

    # @property
    # def option(self):
    #     return self.__option

    # @option.setter
    # def option(self, o):
    #     self.__option = o

    @property
    def name(self):
        return self.__name

    @property
    def note(self):
        return self.__note

    # def add_value(self, value):
    #     util.assert_unique(self.__values, value)
    #     self.__values.append(value)

    @property
    def values(self):
        return self.__values
