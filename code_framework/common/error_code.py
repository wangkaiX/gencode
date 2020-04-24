#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from code_framework.common import tool
from util.python import util


class ErrorConfig:
    def __init__(self, filename, begin_no, end_no):
        self.filename = filename
        self.begin_no = begin_no
        self.end_no = end_no

    def check_no(self, no):
        if 0 == no:
            return
        if no < self.begin_no or no > self.end_no:
            print("配置文件[%s]错误码[%s]超出规定范围[%s~%s]" % (self.filename, no, self.begin_no, self.end_no))
            assert False


class Errno:
    def __init__(self, code, msg, no):
        self.code = code
        self.msg = msg
        self.no = no

    def __eq__(self, o):
        return self.code == o.code or self.msg == o.msg or self.no == o.no


class ErrerCode:
    def __init__(self, filename, begin_no, end_no):
        self.__errno_config = ErrorConfig(filename, begin_no, end_no)
        self.__errnos = []
        # self.__unique_errno_set = set()

    # 返回错误码列表[code msg no]
    @property
    def errnos(self):
        if not self.__errnos:
            self.__parser_config(self.__errno_config)
        return self.__errnos

    def __check_repeat(self, errno):
        if errno in self.__errnos:
            print("重复的错误码[%s]或重复的错误信息[%s]或重复的错误编号[%s]" % (errno.code, errno.msg, errno.no))
            assert False

    def __parser_config(self, config):
        counter = config.begin_no
        util.assert_file(config.filename)
        with open(config.filename, "r") as fp:
            for line in fp.readlines():
                if len(line) == 0 or not line.strip(" \n\r\t") or line[0] == "#":
                    continue
                # line = tool.distinct_str(line, ' ')
                code, msg, no = tool.split(line, None, 3)
                assert code
                assert msg
                if not no:
                    no = counter
                    counter += 1
                else:
                    no = int(no)
                    counter = no + 1
                errno = Errno(code, msg, no)
                config.check_no(no)
                self.__check_repeat(errno)
                self.__errnos.append(errno)
