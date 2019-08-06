#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from mako.template import Template
import util
from gencode.common import meta


def gen_proto(apis, mako_file):
    meta.Type = meta.TypeProto
    util.assert_file(mako_file)
    t = Template(filename=mako_file)
    r = t.render(
        apis=apis,
        enums=meta.Enum.enums(),
        gen_upper_camel=util.gen_upper_camel,
        gen_lower_camel=util.gen_lower_camel,
        gen_underline_name=util.gen_underline_name,
            )
    return r


def gen_code(apis, mako_dir):
    mako_file = os.path.join(mako_dir, 'go', 'grpc', 'grpc.proto')
    return gen_proto(apis, mako_file)
