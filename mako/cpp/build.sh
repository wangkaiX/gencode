#!/bin/bash

export LIBRARY_PATH=${'$'}{PWD}:${'$'}{LIBRARY_PATH}
mkdir docker_build
cd docker_build
mkdir ../install
cmake -DCMAKE_INSTALL_PREFIX=../install ..
make -j4
# make install
