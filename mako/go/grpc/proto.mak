all:
	protoc -I. ${proto_package_name}.proto --go_out=plugins=grpc:.
