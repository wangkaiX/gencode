#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.common import tool
from src.base.generator_base import GeneratorBase
import os
import copy
from util.python import util
# from src.go.errno import GoErrnoGen
import toml


class GeneratorGoBase(GeneratorBase):
    def __init__(self, protocols, **kwargs):  # protocol, mako_dir, errno_out_dir, module_dir, go_src_dir, gen_doc):
        GeneratorBase.__init__(self, protocols, **kwargs)
        go_src_dir = kwargs['go_src_dir']
        self.__package_module_dir = tool.package_name(self.module_dir, go_src_dir)
        self.__package_errno_dir = tool.package_name(self.errno_dir, go_src_dir)

    def gen_code(self):
        self.gen_main()
        self.gen_config()
        self.gen_errno()
        self.gen_init()
        # GeneratorBase.gen_code(self)
        # GeneratorGoBase.gen_init(self)

    def gen_main(self):
        out_file = os.path.join(self.module_dir, 'cmd', 'main.go')
        # if not os.path.exists(out_file):
        mako_file = os.path.join(self.mako_dir, 'go', 'main.go')
        tool.gen_code_file(mako_file, out_file, protocols=self.protocols, package_module_dir=self.__package_module_dir)

    def gen_config(self):
        # config.go
        configs = []
        config_nodes = []
        for p in self.protocols:
            config_nodes += p.config.nodes
            configs.append(p.config)

        nodes = tool.get_all_nodes(config_nodes)
        config = copy.deepcopy(self.protocols[0].config)
        for protocol in self.protocols[1:]:
            config = tool.merge_node(config, protocol.config)
        mako_file = os.path.join(self.mako_dir, 'go', 'config.go')
        out_file = os.path.join(self.module_dir, 'app', 'define', 'config.go')
        tool.gen_code_file(mako_file, out_file, config=config, nodes=nodes, gen_upper_camel=util.gen_upper_camel)
        # config.toml
        config_map = {}
        for config in configs:
            config_map = {**config_map, **(config.value_map)}
        config_text = toml.dumps(config_map)
        mako_file = os.path.join(self.mako_dir, 'go', 'config.toml')
        out_file = os.path.join(self.module_dir, 'configs', 'config.toml')
        tool.gen_code_file(mako_file, out_file, config_text=config_text)

    def gen_errno(self):
        mako_file = os.path.join(self.mako_dir, 'go', 'errno.go')
        # errno_gen = GoErrnoGen(self.errno_configs)
        # errnos = errno_gen.gen_code()
        errno_file = os.path.join(self.errno_dir, 'errno.go')
        package_name = os.path.basename(self.errno_dir)
        tool.gen_code_file(mako_file, errno_file, errnos=self.errnos, package_name=package_name)

    def gen_init(self):
        out_file = os.path.join(self.module_dir, 'cmd', 'init.go')
        if not os.path.exists(out_file):
            mako_file = os.path.join(self.mako_dir, 'go', 'init.go')
            tool.gen_code_file(mako_file, out_file)
