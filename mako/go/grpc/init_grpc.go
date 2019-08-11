package main

import (
	api "${grpc_api_dir}"
	"log"
	"net"
	pb "${proto_dir}"

	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

func InitGrpc() {
	lis, err := net.Listen("tcp", ":20001")
	if err != nil {
		log.Fatal(err)
	}
	s := grpc.NewServer()
	pb.RegisterExampleServer(s, &api.Server{})
	reflection.Register(s)
	err = s.Serve(lis)
	if err != nil {
		log.Fatal(err)
	}
}
