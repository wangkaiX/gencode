package main

import (
	"${project_path}/app/restful_resolver"
	"${project_path}/app/define"
	"fmt"
)

func InitRestful() {
	restful_resolver.Run(fmt.Sprintf("%v:%v", ${restful_ip}, ${restful_port}))
}
