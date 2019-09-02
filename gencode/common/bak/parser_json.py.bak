#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json


class Parser:
    def __init__(self, filename=None, text=None):
        assert bool(filename) ^ bool(text)
        if filename:
            with open(filename, 'r') as f:
                text = f.read()
        self.__text = text
        self.__dict = json.loads(self.__text, object_pairs_hook=dict)

    @property
    def dict(self):
        return self.__dict
