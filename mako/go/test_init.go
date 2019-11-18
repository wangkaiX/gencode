package main

import (
    "${package_service_dir}/app/define"
)

func init() {
    define.InitConfig("../../../configs/config.toml")
}
