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
    % for field in req.fields():
% if field.is_necessary():
    ${field.get_name()}:${field.get_type()._type_graphql}!
% else:
    ${field.get_name()}:${field.get_type()._type_graphql}
% endif
    % endfor
}

% endfor

% for interface_name, req, resp in services:
type ${resp.get_name()} {
    % for field in resp.fields():
    ${field.get_name()}:${field.get_type()._type_graphql}!
    % endfor
}

% endfor

type Query {
% for interface_name, req, resp in services:
    ${interface_name}(${req.get_name()}:${gen_title_name(req.get_name())}!):${resp.get_name()}
% endfor

}

