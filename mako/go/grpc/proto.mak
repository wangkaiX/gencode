all:
	protoc -I. ${proto_package}.proto --go_out=plugins=grpc:.
