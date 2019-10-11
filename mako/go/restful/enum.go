<% import os %>
package ${os.path.basename(restful_define_dir)}
// 不要修改此文件

% for enum in enums:
type ${enum.name} int32

% endfor

const (
% for enum in enums:
	% for i, value in zip(range(0, len(enum.values)), enum.values):
    // ${value.note}
	${enum.name}${value.value} ${enum.name} = ${i}
	% endfor

% endfor
)

% for enum in enums:
var ${enum.name}_name = map[${enum.name}]string {
	% for i, value in zip(range(0, len(enum.values)), enum.values):
    // ${value.note}
	${i} : "${enum.name}${value.value}",
	% endfor
}

% endfor

% for enum in enums:
var ${enum.name}_value = map[string]${enum.name} {
	% for i, value in zip(range(0, len(enum.values)), enum.values):
    // ${value.note}
	"${enum.name}${value.value}" : ${i},
	% endfor
}

% endfor

