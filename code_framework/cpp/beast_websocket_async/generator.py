#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


class Generator:
    def __init__(self, mako_dir, protocol):
        self.__mako_dir = os.path.join(mako_dir, 'cpp', 'websocket')
        self.__protocol = protocol

    def gen(self):
        pass

    def __gen_init(self):
        pass

    def __gen_network_adapt(self):
        pass

    def __gen_network(self):
        pass

    def __gen_api(self):
        pass

    def __gen_types(self):
        pass
