#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# from src.common import tool
from src.base.generator_base import GeneratorBase


class GoGenerator(GeneratorBase):
    def __init__(self, **kwargs):
        GeneratorBase.__init__(self, **kwargs)
        self._server_dir = os.path.join(self._dir, "server")
        self._client_dir = os.path.join(self._dir, "client")
        # server
        self._server_app_dir = os.path.join(self._server_dir, "app")
        self._server_api_dir = os.path.join(self._server_dir, "api")
        self._server_doc_dir = os.path.join(self._server_dir, "docs")
        self._server_cmd_dir = os.path.join(self._server_dir, "cmd")
        self._server_test_dir = os.path.join(self._server_dir, "test")

        # client
        self._client_app_dir = os.path.join(self._client_dir, "app")
        self._client_api_dir = os.path.join(self._client_dir, "api")
        self._client_doc_dir = os.path.join(self._client_dir, "docs")
        self._client_cmd_dir = os.path.join(self._client_dir, "cmd")
        self._client_test_dir = os.path.join(self._client_dir, "test")

        # self._package_dir = tool.package_name(self._dir, self._server_dir)
