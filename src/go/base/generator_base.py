#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.common import tool
from src.base.generator_base import GeneratorBase
import os
import copy
from util.python import util
from src.go.errno import GoErrnoGen
import toml


class GeneratorGoBase(GeneratorBase):
    def __init__(self, protocols, **kwargs):  # protocol, mako_dir, errno_out_dir, service_dir, go_src_dir, gen_doc):
        GeneratorBase.__init__(self, protocols, **kwargs)
        go_src_dir = kwargs['go_src_dir']
        self.__package_service = tool.package_name(self.service_dir, go_src_dir)

    def gen_code(self):
        GeneratorBase.gen_code(self)
        self.gen_init()

    def gen_main(self):
        out_file = os.path.join(self.service_dir, 'cmd', 'main.go')
        # if not os.path.exists(out_file):
        mako_file = os.path.join(self.mako_dir, 'go', 'main.go')
        tool.gen_code_file(mako_file, out_file, protocols=self.protocols, package_service=self.__package_service)

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
            tool.merge_node(config, protocol.config)
        mako_file = os.path.join(self.mako_dir, 'go', 'config.go')
        out_file = os.path.join(self.service_dir, 'app', 'define', 'config.go')
        tool.gen_code_file(mako_file, out_file, config=config, nodes=nodes, gen_upper_camel=util.gen_upper_camel)
        # config.toml
        config_map = {}
        for config in configs:
            config_map = {**config_map, **(config.value_map)}
        config_map = tool.dict_key_clean(config_map)
        config_text = toml.dumps(config_map)
        mako_file = os.path.join(self.mako_dir, 'go', 'config.toml')
        out_file = os.path.join(self.service_dir, 'configs', 'config.toml')
        tool.gen_code_file(mako_file, out_file, config_text=config_text)

    def gen_errno(self):
        errno_mako = os.path.join(self.mako_dir, 'go', 'errno.go')
        errno_gen = GoErrnoGen(errno_mako, self.errno_out_file, self.errno_configs)
        errno_gen.gen_code()

    def gen_init(self):
        out_file = os.path.join(self.service_dir, 'cmd', 'init.go')
        if not os.path.exists(out_file):
            mako_file = os.path.join(self.mako_dir, 'go', 'init.go')
            tool.gen_code_file(mako_file, out_file)
