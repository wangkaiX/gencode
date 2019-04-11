schema {
    query :Query
    mutation :Mutation
}

scalar Time

% for enum in enums:
enum ${enum.name()} {
    % for value, comment in enum.values:
    ${value}  # ${comment}
    % endfor
}

% endfor

% for interface_name, req, resp in services:
input ${req.get_name()} {
    % for field in req.get_fields():
    ${field.get_name()}:${field.get_type()}
    % endfor
}

% endfor

% for interface_name, req, resp in services:
type ${resp.get_name()} {
    % for field in resp.get_fields():
    ${field.get_name()}:${field.get_type()}
    % endfor
}

% endfor

type Query {
% for interface_name, req, resp in services:
    ${interface_name}(${req.get_name()}:${gen_title(req.get_name())}!):${resp.get_name()}
% endfor

}

