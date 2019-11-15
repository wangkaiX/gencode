<% import os %>
package ${package_name}
// 不要修改此文件

% if has_file:
import "mime/multipart"
% endif

% if has_time:
import "time"
% endif
<%
from src.common import meta
%>

% for node in nodes:
// ${node.type.go} ${node.note}
type  ${node.type.go} struct {
% for field in node.fields + node.nodes:
    <%
    if isinstance(field, meta.Node):
        _type = '[]' * field.dimension + "*" + field.type.go
    else:
        _type = '[]' * field.dimension + field.type.go
    if field.required:
        required = ' binding:"required"'
    else:
        required = ''
    if field.type.is_file:
        continue
    %>
    ${gen_upper_camel(field.name)} ${_type} `form:"${field.name}" json:"${field.name}"${required}`// ${field.note}

% endfor

}

% endfor

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
