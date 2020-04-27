#!/bin/bash

export LIBRARY_PATH=${'$'}{PWD}:${'$'}{LIBRARY_PATH}
mkdir docker_build
cd docker_build
mkdir ../install
cmake -DCMAKE_INSTALL_PREFIX=../install ..
LOGICAL_NUM=`cat /proc/cpuinfo | grep "processor" | wc -l`
PHYSICAL_NUM=`cat /proc/cpuinfo | grep "physical id" | uniq | wc -l`
# 有些物理核心与逻辑核心数一样，编译时会崩溃，可能是内存不够，这种情况线程数 /2
if [ ${'$'}{PHYSICAL_NUM} -eq ${'$'}{LOGICAL_NUM} ]
then
    PHYSICAL_NUM=$(expr ${'$'}{PHYSICAL_NUM} / 2)
    if [ ${'$'}{PHYSICAL_NUM} -lt 1 ] 
    then
        PHYSICAL_NUM=1
    fi
fi
make -j${'$'}{PHYSICAL_NUM}
# make install
