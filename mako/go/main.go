package main
// 不要修改此文件

import (
    "flag"
	"fmt"

	// "log"
    "${package_service_dir}/app/define"
)

var configFile string

func main() {
    flag.StringVar(&configFile, "configfile", "configs/config.toml", "配置文件路径")
    flag.Parse()
    define.InitConfig(configFile)
	fmt.Printf("%+v\n", define.Cfg)
    Init()
<%
from src.common import code_type
%>
% for protocol in protocols:
	% if protocol.framework_type == code_type.grpc:
	go InitGrpc()
	% elif protocol.framework_type == code_type.go_gin:
	go InitGin()
	% endif
% endfor
	select {}

}
