#!/bin/bash

# export LIBRARY_PATH=${'$'}{PWD}:${'$'}{LIBRARY_PATH}
mkdir build
cd build
mkdir ../install
cmake -DCMAKE_INSTALL_PREFIX=../install ..
# LOGICAL_NUM=`cat /proc/cpuinfo | grep "processor" | wc -l`
PHYSICAL_NUM=`cat /proc/cpuinfo | grep "physical id" | uniq | wc -l`
# 有些物理核心过多，编译时会崩溃，可能是内存不够
MemAvailable=${'$'}(cat /proc/meminfo | grep MemAvailable | tr -cd "[0-9]")
MemAvailable=${'$'}(expr ${'$'}{MemAvailable} / 800 / 1024)
if [ ${'$'}{MemAvailable} -le 0 ]
then
    PHYSICAL_NUM=1
elif [ ${'$'}{PHYSICAL_NUM} -ge ${'$'}{MemAvailable} ]
then
    PHYSICAL_NUM=${'$'}{MemAvailable}
fi

echo "make -j${'$'}{PHYSICAL_NUM} VERBOSE=1"
make -j${'$'}{PHYSICAL_NUM} VERBOSE=1
# make install
