package main

import (
	"${package_restful_api_dir}"
	"${package_project_dir}/app/define"
	"fmt"
)

func InitRestful() {
	restful_resolver.Run(fmt.Sprintf("%v:%v", define.Cfg.RestfulIP, define.Cfg.RestfulPort))
}
