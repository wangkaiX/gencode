dev_image=registry.cn-shanghai.aliyuncs.com/love996/ubuntu2004:dev
repo=registry.cn-shanghai.aliyuncs.com/love996/sl
tag_dev=${service_name}_dev
# release_image=registry.cn-shanghai.aliyuncs.com/love996/centos:release
# dev=dev
# release=release

uid=$(shell id -u)
gid=$(shell id -g)

build_dev:
	docker run --rm \
	           -v ${'$'}{PWD}:${'$'}{PWD} \
			   -v /tmp/docker_ccache:/tmp/ccache \
			   -v ${'$'}{PWD}/docker_build:${'$'}{PWD}/build \
               -w ${'$'}{PWD} \
               ${'$'}{dev_image} \
               bash build.sh

dev:build_dev
	docker build -t ${'$'}{repo}:${'$'}{tag_dev} .
	docker push ${'$'}{repo}:${'$'}{tag_dev}
