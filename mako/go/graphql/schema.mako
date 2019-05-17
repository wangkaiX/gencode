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
    % if st.is_req():
        <%
            type = 'input'
        %>
    % elif st.is_resp():
        <%
            type = 'type'
        %>
    % endif
${type} ${st.get_name()} {
    % for field in st.fields():
        % if (st.is_resp() and not field.is_object()) or field.is_necessary() :
            <%
                flag = '!'
            %>
        % elif st.is_req() or field.is_object():
            <%
                flag = ''
            %>
        % endif
 
        % if field.is_list():
    ${field.get_name()}:[${field.get_type()._graphql}${flag}]${flag}
        % else:
    ${field.get_name()}:${field.get_type()._graphql}${flag}
        % endif
    % endfor
}

% endfor




type Query {
% for interface in all_interface:
    % if interface.get_name() in query_list:
    <%
    req = interface.get_req()
    resp = interface.get_resp()
    %>
        % if len(req.fields()) > 0:
    ${interface.get_name()}(${req.get_name()[0].lower()}${req.get_name()[1:]}:${gen_title_name(req.get_name())}):${resp.get_name()}
        % else:
    ${interface.get_name()}():${resp.get_name()}
        % endif
    % endif
% endfor

}

type Mutation{
% for interface in all_interface:
    <%
    req = interface.get_req()
    resp = interface.get_resp()
    %>
    % if interface.get_name() not in query_list:
        % if len(req.fields()):
    ${interface.get_name()}(${req.get_name()[0].lower()}${req.get_name()[1:]}:${gen_title_name(req.get_name())}):${resp.get_name()}
        % else:
    ${interface.get_name()}():${resp.get_name()}
        % endif
    % endif
% endfor

}
