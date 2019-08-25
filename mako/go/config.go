package define

import (
    "github.com/BurntSushi/toml"
)

type Config struct {
% for config in configs:
	${gen_upper_camel(config.name)} struct {
	% for field in config.fields:
		${gen_upper_camel(field.name)} ${field.type.name} `toml:"${field.name}"`
	% endfor
} `toml:"${config.name}"`

% endfor
}

var Cfg = new(Config)

func LoadConfig(filename string, v interface{}) error {
    _, err := toml.DecodeFile(filename, v)
    return err 
}

