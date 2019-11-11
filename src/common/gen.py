#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# import shutil
from src.common import parser_config
import util.python.util as util
from src.common import tool
from src.common import meta
from src.common import field_type
from src.go.grpc import gen as go_grpc_gen
from src.go.restful import gen as go_restful_gen
from src.common import errno
# import markdown
# import codecs
# from gencode import cpp


def gen_server():
    pass


def gen_client():
    pass


def gen_test():
    pass


def save_file(filename, txt):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filename, 'wb') as f:
        f.write(txt)


def go_fmt(filename):
    cmd = "go fmt %s" % filename
    r = os.popen(cmd)
    r.read()
    # r.close()
    # os.system(cmd)


def check_args(
            filename,
            code_type,
            project_dir,
            errno_out_dir,
            # service_name,
            main_dir,
            mako_dir,
            graphql_dir=None,
            graphql_schema_dir=None,
            graphql_define_pkg_name=None,
            graphql_resolver_pkg_name=None,
            ip=None,
            port=None,
            restful_api_dir=None,
            restful_define_dir=None,
            grpc_proto_dir=None,
            grpc_service_name=None,
            grpc_service_type=None,
            # grpc_service_dir=None,
            grpc_package=None,
            proto_package=None,
            grpc_api_dir=None,
            # grpc_define_pkg_name="Server",
            # gen_server=None,
            # gen_client=None,
            # gen_test=None,
            **kwargs,
            ):
    if code_type not in field_type.language_types:
        print("仅支持[%s]" % field_type.language_types)
        assert False
    assert gen_server or gen_client or gen_test
    assert mako_dir

    # return protocols

'''
    apis, protocol, configs, config_map = parser_config.gen_apis(filename)
    if protocol.type == meta.proto_graphql:
        assert graphql_dir and \
               graphql_schema_dir and \
               graphql_define_pkg_name and \
               graphql_resolver_pkg_name
    elif protocol.type == meta.proto_http:
        assert restful_api_dir and \
               restful_define_dir
    elif protocol.type == meta.proto_grpc:
        assert grpc_proto_dir and \
               grpc_api_dir and \
               grpc_service_name and \
               grpc_service_type and \
               proto_package
    else:
        print("未知的协议[%s]" % protocol)
        assert False

    return apis, protocol, configs, config_map
'''


def __gen_code_file(
            filename,
            code_type,
            **kwargs,
            ):
    meta.Node.clear()
    meta.Enum.clear()
    apis, protocol, configs, config_map = check_args(filename, code_type, **kwargs)

    nodes = meta.Node.req_resp_nodes()
    types = set([node.type.name for node in nodes])
    unique_nodes = []
    for node in nodes:
        if node.type.name in types:
            unique_nodes.append(node)
            types.remove(node.type.name)

    kwargs['nodes'] = unique_nodes
    kwargs['enums'] = meta.Enum.enums()
    kwargs['apis'] = apis
    kwargs['protocols'].append(protocol)
    kwargs['configs'] += configs
    kwargs['config_map'] = dict(kwargs['config_map'], **config_map)

    if code_type in meta.code_go:
        if protocol.type == meta.proto_grpc:
            go_grpc_gen.gen_code_file(**kwargs)
        elif protocol.type == meta.proto_http:
            go_restful_gen.gen_code_file(**kwargs)
    elif code_type in meta.code_cpp:
        pass
    else:
        print("不支持的语言[%s]" % (code_type))
        assert False
    # doc
    return apis, protocol, kwargs['configs'], kwargs['config_map']


def gen_doc(**kwargs):
    tags = [api.doc_tag for api in kwargs['apis']]
    tags.append('')
    for tag in tags:
        gen_tag_doc(tag, **kwargs)


def gen_tag_doc(doc_tag, **kwargs):
    # doc
    if doc_tag:
        apis = kwargs['apis']
        apis = [api for api in apis if api.doc_tag == doc_tag]
        kwargs['apis'] = apis
        filename = "%s_%s" % (os.path.basename(kwargs['project_dir']), doc_tag)
    else:
        filename = os.path.basename(kwargs['project_dir'])
    out_file = os.path.join(kwargs['project_dir'], 'doc', filename + ".md")
    out_html_file = os.path.join(kwargs['project_dir'], 'doc', filename + ".html")
    tool.gen_code_file(os.path.join(kwargs['mako_dir'], 'go', 'doc.md'),
                       out_file,
                       dict2json=tool.dict2json,
                       **kwargs)
    input_file = codecs.open(out_file, mode="r", encoding="utf-8")
    html = markdown.markdown(input_file.read())
    output_file = codecs.open(out_html_file, mode="w", encoding="utf-8")
    output_file.write(html)


def gen_code_files(filenames):
    protocols = []
    for filename in filenames:
        protocols.append(meta.Protocol(filename))
    kwargs['protocols'] = []
    kwargs['configs'] = []
    kwargs['config_map'] = {}
    kwargs['gen_upper_camel'] = util.gen_upper_camel
    kwargs['gen_lower_camel'] = util.gen_lower_camel
    kwargs['gen_underline_name'] = util.gen_underline_name
    code_type = code_type.upper()
    kwargs['mako_dir'] = util.abs_path(kwargs['mako_dir'])
    kwargs['error_package'] = tool.package_name(kwargs["error_out_dir"], kwargs["go_src"])
    kwargs['apis'] = []
    for filename in filenames:
        util.assert_file(filename)
        apis, protocol, configs, config_map = __gen_code_file(filename, code_type, **kwargs)
        kwargs['configs'] = configs
        kwargs['config_map'] = config_map
        kwargs['apis'] += apis

    if code_type in meta.code_go:
        # error.go
        out_file = os.path.join(kwargs["error_out_dir"], "error.go")
        print(out_file)
        gen = error.GoGen(kwargs['mako_dir'], kwargs["error_config_file"], kwargs["errno_begin"], kwargs["errno_end"],
                          out_file,
                          )
        gen.gen()
        tool.go_fmt(out_file)

        # config.toml
        out_file = os.path.join(kwargs['project_dir'], 'configs', 'config.toml')
        tool.gen_code_file(os.path.join(kwargs['mako_dir'], 'go', 'config.toml'),
                           out_file,
                           **kwargs,
                           )

        # config.go
        out_file = os.path.join(kwargs['project_dir'], 'app', 'define', 'config.go')
        tool.gen_code_file(os.path.join(kwargs['mako_dir'], 'go', 'config.go'),
                           out_file,
                           **kwargs,
                           )
        tool.go_fmt(out_file)

        # init
        out_file = os.path.join(kwargs['project_dir'], 'cmd', 'init.go')
        if not os.path.exists(out_file):
            tool.gen_code_file(os.path.join(kwargs['mako_dir'], 'go', 'init.go'),
                               out_file,
                               **kwargs)
            tool.go_fmt(out_file)

        # main
        out_file = os.path.join(kwargs['main_dir'], 'main.go')
        tool.gen_code_file(os.path.join(kwargs['mako_dir'], 'go', 'main.go'),
                           out_file,
                           package_project_dir=tool.package_name(kwargs['project_dir'], kwargs['go_src']),
                           **kwargs)
        tool.go_fmt(out_file)

        # doc
        print("len apis:", len(apis))
        gen_doc(**kwargs)

    else:
        print("不支持的语言[%s]" % (code_type))
        assert False
