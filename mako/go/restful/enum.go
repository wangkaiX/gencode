package define

const (
% for enum in enums:
	% for i, value in zip(range(0, len(enum.value)), enum.value):
	${enum.name}${value} int32 = ${i}
	% endfor

% endfor
)

% for enum in enums:
var ${enum.name}_name = map[int32]string {
	% for i, value in zip(range(0, len(enum.value)), enum.value):
	${i} : "${enum.name}${value}",
	% endfor
}

% endfor

