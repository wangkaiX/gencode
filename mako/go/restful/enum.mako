package define

const (
% for enum in all_enum:
    <%
    values = enum.get_values()
    %>
    % for i in range(0, len(values)):
    // ${enum.get_name()}${values[i].get_value()} ...
    ${enum.get_name()}_${values[i].get_value()} = ${i} // ${values[i].get_comment()}
    % endfor

% endfor
)

