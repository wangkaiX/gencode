<% import os %>
package ${os.path.basename(graphql_define_dir)}

const (
% for enum in enums:
    % for value in enum.values:
    ${enum.name}_${value} = "${value}" 
    % endfor

% endfor
)

