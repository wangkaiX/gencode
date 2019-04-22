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

<%def name='getflag(field)'>
    % if field.is_necessary():
        <% return '!' %>
    % endif
</%def>

% for req in reqs:
    % if req:
input ${req.get_name()} {
        % for field in req.fields():
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

    % endif
% endfor

% for resp in resps:
type ${resp.get_name()} {
    % for field in resp.fields():
        % if field.is_list():
            % if field.is_object():
    ${field.get_name()}:[${field.get_base_type()}]
            % else:
    ${field.get_name()}:[${field.get_base_type()}!]!
            % endif
        % else:
    ${field.get_name()}:${field.get_type()._graphql}!
        % endif
    % endfor
}

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
