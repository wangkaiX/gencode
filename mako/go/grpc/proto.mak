all:
	protoc -I. ${package_name}.proto --go_out=plugins=grpc:.
