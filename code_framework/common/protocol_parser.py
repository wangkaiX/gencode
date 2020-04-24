#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from src.common import tool
# from src.common import meta
# import util.python.util as util
# from abc import abstractmethod
import json5
import toml
import os


class ParserBase:
    def __init__(self, filename=None, fp=None, text=None):
        if (int(bool(filename)) + int(bool(fp)) + int(bool(text))) != 1:
            print("参数有误", filename, fp, text)
            assert False
        self.filename = filename
        self.fp = fp
        self.text = text
        print("base parser")

    # @abstractmethod
    def parse(self):
        if self.filename:
            self.__parse_file()
        elif self.fp:
            self.__parse_fp()
        return self._parse_text()

    def __parse_file(self):
        self.fp = open(self.filename, "rb")
        self.__parse_fp()

    def __parse_fp(self):
        self.text = self.fp.read()
        self._parse_text()

    # @abstractmethod
    def _parse_text(self):
        assert False

    def _parse_dict(self):
        assert False


class Json5(ParserBase):
    def __init__(self, filename=None, fp=None, text=None):
        ParserBase.__init__(self, filename, fp, text)

    # @abstractmethod
    def _parse_text(self):
        return json5.loads(self.text)


class Toml(ParserBase):
    def __init__(self, filename=None, fp=None, text=None):
        ParserBase.__init__(self, filename, fp, text)

    # @abstractmethod
    def _parse_text(self):
        return toml.loads(self.text)


class Parser:
    def __init__(self, filename):
        self.__filename = filename

    def __get_parser(self, filename):
        ext = os.path.splitext(filename)
        if len(ext) == 0:
            print(filename, ext)
            assert False
        ext = ext[-1]
        if ext in ['.json', '.json5']:
            ret = Json5(filename)
        elif ext in ['toml']:
            ret = Toml(filename)
        else:
            print("不支持的文件类型[%s]", filename)
            assert False
        return ret

    def parse(self):
        return self.__get_parser(self.__filename).parse()
