<% import os %>
package ${os.path.basename(restful_define_dir)}

% for enum in enums:
type ${enum.name} int32

% endfor

const (
% for enum in enums:
	% for i, value in zip(range(0, len(enum.values)), enum.values):
	${enum.name}${value} ${enum.name} = ${i}
	% endfor

% endfor
)

% for enum in enums:
var ${enum.name}_name = map[${enum.name}]string {
	% for i, value in zip(range(0, len(enum.values)), enum.values):
	${i} : "${enum.name}${value}",
	% endfor
}

% endfor

% for enum in enums:
var ${enum.name}_value = map[string]${enum.name} {
	% for i, value in zip(range(0, len(enum.values)), enum.values):
	"${enum.name}${value}" : ${i},
	% endfor
}

% endfor

