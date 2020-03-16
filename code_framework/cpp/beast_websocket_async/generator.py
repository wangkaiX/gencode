#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


class Generator:
    def __init__(self, mako_dir, protocol):
        self.__mako_dir = os.path.join(mako_dir, 'cpp', 'websocket')
        self.__protocol = protocol

    def _gen_network_adapt(self):
        pass
