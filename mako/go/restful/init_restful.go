package main
// 不要修改此文件

import (
	"${package_restful_api_dir}"
	"${package_project_dir}/app/define"
	"fmt"
)

func InitRestful() {
	<% import os %>
	${os.path.basename(package_restful_api_dir)}.Run(fmt.Sprintf("%v:%v", define.Cfg.HttpAddr.Ip, define.Cfg.HttpAddr.Port))
}
