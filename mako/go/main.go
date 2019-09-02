package main

import (
    "flag"
	"fmt"

	"log"
    "${package_project_dir}/app/define"
)

var configFile string

func reloadConfig() error {
    err := define.LoadConfig(configFile, define.Cfg)
    return err 
}

func main() {
    flag.StringVar(&configFile, "configfile", "configs/config.toml", "配置文件路径")
    flag.Parse()
    err := reloadConfig()
    if err != nil {
        log.Fatal(err)
    }
	fmt.Printf("%+v\n", define.Cfg)
<%
from gencode.common import meta
%>
% for protocol in protocols:
	% if protocol.type == meta.proto_grpc:
	go InitGrpc()
	% elif protocol.type == meta.proto_http:
	go InitRestful()
	% endif
% endfor
	select {}

}
