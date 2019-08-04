#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from mako.template import Template
import util
from gencode.common import meta


def gen_proto(mako_file, apis, nodes, enums):
    meta.Type = meta.TypeProto
    util.assert_file(mako_file)
    t = Template(filename=mako_file)
    r = t.render(
        apis=apis,
        nodes=nodes,
        enums=enums,
        gen_upper_camel=util.gen_upper_camel
            )
    return r
