#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.common import tool
from util.python import util


class ErrnoConfig:
    def __init__(self, filename, begin_no, end_no):
        self.filename = filename
        self.begin_no = begin_no
        self.end_no = end_no

    def check_no(self, no):
        if no < self.begin_no or no > self.end_no:
            print("错误码[%s]超出规定范围", no)
            assert False


class Errno:
    def __init__(self, code, msg, no):
        self.__code = code
        self.__msg = msg
        self.__no = no


class ErrnoGen:
    # def __init__(self, mako_file, out_file, errno_configs):
    def __init__(self, errno_configs):
        # self.__mako_file = mako_file
        # self.__out_file = out_file
        self.__errno_configs = errno_configs
        self.__errnos = []
        self.__unique_errno_set = set()

    def __check_repeat(self, errno):
        if errno.no in self.__unique_errno_set or errno.code in self.__unique_errno_set:
            print("重复的错误码[%s]或重复的错误信息[%s]或重复的错误编号[%s]" % (errno.code, errno.msg, errno.no))
            assert False
        self.__unique_errno_set.add(errno.code)
        self.__unique_errno_set.add(errno.msg)
        self.__unique_errno_set.add(errno.no)

    def __parser_config(self, config):
        counter = config.begin_no
        util.assert_file(config.filename)
        with open(config.filename, "rb") as fp:
            for line in fp.readlines():
                if len(line) == 0 or line.strip(" \n\r\t") == "" or line[0] == "#":
                    continue
                # line = tool.distinct_str(line, ' ')
                code, msg, no = tool.split(line, None, 3)
                assert code
                assert msg
                errno = Errno(code, msg, no)
                self.__check_repeat(errno)
                self.__errnos.append(errno)
                if not no:
                    no = counter
                    counter += 1
                else:
                    no = int(no)
                    counter = no + 1

    def parser(self):
        for errno_config in self.__errno_configs:
            self.__parser_config(errno_config)
