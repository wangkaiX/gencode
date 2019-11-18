package main
// 不要修改此文件

import (
	"${package_api}"
	"${package_service_dir}/app/define"
	"fmt"
)

func InitGin() {
	<% import os %>
	${os.path.basename(package_api)}.Run(fmt.Sprintf("%v:%v", define.Cfg.HttpAddr.Ip, define.Cfg.HttpAddr.Port))
}
