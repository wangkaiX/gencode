all:
	protoc -I. ${service_name}.proto --go_out=plugins=grpc:.
