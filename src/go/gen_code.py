#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from src.go import errno
from src.common import tool
from src.common import doc


class GenGoCode:
    def __init__(self, protocol, **kwargs):  # protocol, mako_dir, errno_out_dir, project_dir, go_src_dir, gen_doc):
        self.__mako_dir = kwargs['mako_dir']
        self.__errno_out_file = kwargs['errno_out_file']
        self.__service_dir = kwargs['service_dir']
        self.__go_src_dir = kwargs['go_src_dir']
        self.__gen_doc = kwargs['gen_doc']
        self.__errno_configs = kwargs['errno_configs']
        self.__protocol = protocol
        self.__package_project = tool.package_name(self.__project_dir, self.__go_src_dir)
        self.__service_name = kwargs['service_name']

    def gen_code(self):
        self.gen_errno_code()
        self.gen_config()
        self.gen_init()
        self.gen_main()
        self.gen_doc()

    def gen_errno_code(self):
        errno_mako = os.path.join(self.__mako_dir, 'go', 'errno.go')
        errno_gen = errno.GoErrnoGen(errno_mako, self.__errno_out_file, self.__errno_configs)
        errno_gen.gen_code()

    def gen_config(self):
        # config.go
        mako_file = os.path.join(self.__mako_dir, 'go', 'config.go')
        out_file = os.path.join(self.__project_dir, 'app', 'define', 'config.go')
        tool.gen_code_file(mako_file, out_file, configs=self.__protocol.configs)
        # config.toml
        mako_file = os.path.join(self.__mako_dir, 'go', 'config.toml')
        out_file = os.path.join(self.__project_dir, 'configs', 'config.toml')
        tool.gen_code_file(mako_file, out_file, configs=self.__protocol.configs)

    def gen_init(self):
        out_file = os.path.join(self.__project_dir, 'cmd', 'init.go')
        if not os.path.exists(out_file):
            mako_file = os.path.join(self.__mako_dir, 'go', 'init.go')
            tool.gen_code_file(mako_file, out_file)

    def gen_main(self):
        out_file = os.path.join(self.__project_dir, 'cmd', 'main.go')
        if not os.path.exists(out_file):
            mako_file = os.path.join(self.__mako_dir, 'go', 'main.go')
            tool.gen_code_file(mako_file, out_file, protocols=self.__protocols, package_project=self.__package_project)

    def gen_doc(self):
        mako_file = os.path.join(self.__mako_dir, 'doc.md')
        doc_name = self.__service_name
        doc_dir = os.path.join(self.__service_dir, 'doc')
        d = doc.Doc(mako_file, doc_name, doc_dir, self.__apis)
        d.gen_doc()
