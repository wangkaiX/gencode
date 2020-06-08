package main
// 不要修改此文件

import (
	api "${package_api_dir}"
	"log"
	"net"
	"fmt"
	pb "${package_proto_dir}"
	"${package_service_dir}/app/define"

	"google.golang.org/grpc"
	// "google.golang.org/grpc/reflection"
)

func InitGrpc() {
	lis, err := net.Listen("tcp", fmt.Sprintf(":%v", define.Cfg.GrpcAddr.Port))
	if err != nil {
		log.Fatal(err)
	}
	s := grpc.NewServer()
	pb.Register${grpc_module_name}Server(s, &api.Server{})
	// reflection.Register(s)
	err = s.Serve(lis)
	if err != nil {
		log.Fatal(err)
	}
}
