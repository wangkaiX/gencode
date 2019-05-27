package graphqldefine

const (
% for enum in all_enum:
    % for value in enum.get_values():
    // ${enum.get_name()}${value.get_value()} ...
    ${enum.get_name()}_${value.get_value()} = "${value.get_value()}" // ${value.get_comment()}
    % endfor

% endfor
)

