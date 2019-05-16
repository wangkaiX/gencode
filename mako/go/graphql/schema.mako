schema {
    query :Query
    mutation :Mutation
}

scalar Time

% for interface in all_interface:
    % for enum in interface.get_enums():
enum ${enum.get_name()} {
    % for v in enum.get_values():
    ${v.get_value()} # ${v.get_comment()}
    % endfor
}
    %endfor

% endfor

% for st in all_type:
    % if k in inputs:
input ${t.get_name()} {
        % for field in t.fields():
            % if field.is_necessary():
                <%
                    flag = '!'
                %>
            % else:
                <%
                    flag = ''
                %>
            % endif
    ${field.get_name()}:${field.get_type()._graphql}${flag}
        % endfor
}

    % else:
type ${t.get_name()} {
    % for field in t.fields():
        % if field.is_list():
            % if field.is_object():
    ${field.get_name()}:[${field.get_base_type()._graphql}]
            % else:
    ${field.get_name()}:[${field.get_base_type()._graphql}!]!
            % endif
        % else:
    ${field.get_name()}:${field.get_type()._graphql}!
        % endif
    % endfor
}

    % endif
% endfor




type Query {
% for interface_name, req, resp in services:
    % if interface_name in query_list:
        % if req:
    ${interface_name}(${req.get_name()[0].lower()}${req.get_name()[1:]}:${gen_title_name(req.get_name())}):${resp.get_name()}
        % else:
    ${interface_name}():${resp.get_name()}
        % endif
    % endif
% endfor

}

type Mutation{
% for interface_name, req, resp in services:
    % if interface_name not in query_list:
        % if req:
    ${interface_name}(${req.get_name()[0].lower()}${req.get_name()[1:]}:${gen_title_name(req.get_name())}):${resp.get_name()}
        % else:
    ${interface_name}():${resp.get_name()}
        % endif
    % endif
% endfor

}
