#!/bin/bash

# 本地生成目录
dst_dir="${GOPATH}/src/example"
# docker go path
docker_go_path=/tmp/gopath
# docker中生成的目录(与dst_dir是映射目录)
docker_dst_dir="${docker_go_path}/src/example"

# 下面不用修改
gencode_path=/tmp/gencode
cmd="python3 example.py"
uid=$(id -u)

mkdir ${dst_dir}

docker run -it --env GOPATH=${docker_go_path} \
               --env HOME=/tmp \
           -u ${uid}:${uid} \
           -v ${dst_dir}:${docker_dst_dir} \
           -v ${PWD}:${gencode_path} \
           --workdir ${gencode_path} \
           w505703394/alpine:python3 \
           ${cmd}
