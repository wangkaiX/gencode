#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from src.common import tool
# from src.common import meta
# import util.python.util as util
# from abc import abstractmethod
import json5


class Parser:
    def __init__(self, filename=None, fp=None, text=None):
        if (int(bool(filename)) + int(bool(fp)) + int(bool(text))) != 1:
            print("参数有误", filename, fp, text)
            assert False
        self.filename = filename
        self.fp = fp
        self.text = text
        print("base parser")

    # @abstractmethod
    def parser(self):
        if self.filename:
            self.__parser_file()
        elif self.fp:
            self.__parser_fp()
        return self.parser_text()

    def __parser_file(self):
        self.fp = open(self.filename, "rb")
        self.__parser_fp()

    def __parser_fp(self):
        self.text = self.fp.read()
        self.parser_text()

    # @abstractmethod
    def parser_text(self):
        assert False

    def parser_dict(self):
        assert False


class Json5(Parser):
    def __init__(self, filename=None, fp=None, text=None):
        Parser.__init__(self, filename, fp, text)

    # @abstractmethod
    def parser_text(self):
        return json5.loads(self.text)
