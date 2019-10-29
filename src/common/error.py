#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mako.template import Template
import os
from gencode.common import meta
# from gencode.common import tool
import util.python.util as util


class GoGen:
    def __init__(self, mako_dir, error_file, begin_no, end_no, out_file):
        self.mako_dir = mako_dir
        self.err_infos = []
        self.error_file = error_file
        self.begin_no = begin_no
        self.end_no = end_no
        self.out_file = out_file
        self.package_name = os.path.basename(os.path.dirname(out_file))

    def append(self, err_info):
        if err_info not in self.err_infos:
            self.err_infos.append(err_info)

    def gen(self):
        print("error_file:", self.error_file)
        util.assert_file(self.error_file)

        f = open(self.error_file, encoding='utf8')
        ls = f.readlines()
        counter = self.begin_no

        def check_number(number, begin, end):
            if 0 != number:
                assert number >= begin and number <= end

        for l in ls:
            if l.strip(" \n\r\t") == "" or l[0] == "#":
                continue

            err_line = l.split()
            assert len(err_line) > 1
            if 2 == len(err_line):
                code, msg = err_line
                check_number(counter, self.begin_no, self.end_no)
                number = counter
                self.append(meta.ErrorInfo(code, msg, number))
                counter = counter + 1
            elif 3 == len(err_line):
                code, msg, number = err_line
                number = int(number)
                check_number(number, self.begin_no, self.end_no)
                self.append(meta.ErrorInfo(code, msg, number))
                counter = number + 1

        # curr_path = os.path.split(os.path.realpath(__file__))[0] + "/../"
        mako_file = os.path.join(self.mako_dir,  "go", "error.go")
        util.assert_file(mako_file)
        t = Template(filename=mako_file, input_encoding="utf8")
        s = t.render(err_infos=self.err_infos, package_name=self.package_name)
        d = os.path.dirname(self.out_file)
        if not os.path.exists(d):
            os.makedirs(d)
        print("error_out_file:", self.out_file)
        with open(self.out_file, "w", encoding='utf8') as f:
            f.write(s)
        return s
