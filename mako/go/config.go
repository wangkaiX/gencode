package define
// 不要修改此文件

import (
    "github.com/BurntSushi/toml"
)

% for node in nodes:
type ${node.type.go} struct {
% for member in node.nodes + node.fields:
    ${gen_upper_camel(member.name)} ${member.type.go} `toml:"${member.name}"`
% endfor
}

% endfor

type Config struct {
% for member in config.nodes + config.fields:
    ${gen_upper_camel(member.name)} ${member.type.go} `toml:"${member.name}"`
% endfor
}

var Cfg = new(Config)

func InitConfig(filename string) {
    _, err := toml.DecodeFile(filename, Cfg)
    if err != nil {
        panic(err)
    }
}
