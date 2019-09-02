package ${graphql_define_package_name}

const (
% for enum in enums:
    % for value in enum.values:
    ${enum.name}_${value} = "${value}" 
    % endfor

% endfor
)

