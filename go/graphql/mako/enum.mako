package define

% for k, v in enums.items():
const (
% for e in v:
    ${e} = "${e}"
% endfor
)

% endfor
