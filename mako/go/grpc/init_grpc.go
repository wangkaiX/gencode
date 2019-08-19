package main

import (
	api "${package_grpc_api_dir}"
	"log"
	"net"
	pb "${package_grpc_proto_dir}"

	"google.golang.org/grpc"
	// "google.golang.org/grpc/reflection"
)

func InitGrpc() {
	lis, err := net.Listen("tcp", ":20001")
	if err != nil {
		log.Fatal(err)
	}
	s := grpc.NewServer()
	pb.Register${grpc_service_name}Server(s, &api.Server{})
	// reflection.Register(s)
	err = s.Serve(lis)
	if err != nil {
		log.Fatal(err)
	}
}
