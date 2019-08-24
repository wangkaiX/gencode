package main

import (
    "flag"

	"log"
    "${package_project_path}/app/define"
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
}
