package main

import (
	"${package_restful_api_dir}"
	"${package_project_dir}/app/define"
	"fmt"
)

func InitRestful() {
	<% import os %>
	${os.path.basename(package_restful_api_dir)}.Run(fmt.Sprintf("%v:%v", define.Cfg.RestfulIP, define.Cfg.RestfulPort))
}
