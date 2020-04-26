dev_image=registry.cn-shanghai.aliyuncs.com/love996/ubuntu2004:dev
repo=registry.cn-shanghai.aliyuncs.com/love996/sl
tag_dev=${project_name}_dev
# release_image=registry.cn-shanghai.aliyuncs.com/love996/centos:release
# dev=dev
# release=release

build_dev:
	docker run --rm -v ${'$'}{PWD}:${'$'}{PWD} \
                                -w ${'$'}{PWD} \
                                ${'$'}{dev_image} \
                        bash build.sh

dev:build_dev
	docker build -t ${'$'}{repo}:${'$'}{tag_dev} .
	docker push ${'$'}{repo}:${'$'}{tag_dev}
