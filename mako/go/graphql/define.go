<% import os %>
package ${os.path.basename(graphql_define_dir)}

% for field in api.fields():
    % if 'time.Time' == field.type.name:
import "time"
        <% break %>
    % endif
% endfor
<%
from gencode.common import meta
%>

// ${api.name} ${api.note}
type  ${gen_upper_camel(api.type.name)} struct {
% for field in api.fields:
    <%
    if field.is_required or api.is_resp:
          flag = ''
    else:
          flag = '*'
    if field.type.name in [enum.name for enum in meta.Enum.enums()]:
        _type = 'string'
    else:
        _type = field.type.name
    %>
    % if field.dimension > 0:
    ${gen_upper_camel(field.name)} ${flag}[]${_type} // ${field.note}
    % else:
    ${gen_upper_camel(field.name)} ${flag}${_type} // ${field.note}
    % endif

% endfor
% for node in api.nodes:
    <%
    if (node.dimension > 0 and node[0].is_resp) or (node.dimension == 0 and node.is_resp):
          flag = ''
    else:
          flag = '*'
    %>
    % if node.dimension > 0:
    ${gen_upper_camel(node[0].name)} ${flag}[]${flag}${node[0].type.name} // ${node[0].note}
    % else:
    ${gen_upper_camel(node.name)} ${flag}${node.type.name} // ${node.note}
    % endif

% endfor
}

##% if api.is_req:
##func ToDefine${st.get_name()}(input *${st.get_name()}) (*define.${st.get_name()}) {
##    output := define.${st.get_name()}{}
##    if input == nil {
##        return &output
##    }
##    % for field in st.fields():
##        % if not field.is_necessary():
##    if input.${gen_upper_camel(field.get_name())} != nil {
##        output.${gen_upper_camel(field.get_name())} = *input.${gen_upper_camel(field.get_name())}
##    }
##        % else:
##    output.${gen_upper_camel(field.get_name())} = input.${gen_upper_camel(field.get_name())}
##        % endif
##    % endfor
##    % for node in st.get_nodes():
##        % if type(node) == list:
##    if input.${gen_upper_camel(node[0].get_field_name())} != nil {
##        for _, arg := range(*input.${gen_upper_camel(node[0].get_field_name())}) {
##            output.${gen_upper_camel(node[0].get_field_name())} = append(output.${gen_upper_camel(node[0].get_field_name())}, *ToDefine${node[0].get_name()}(arg))
##        }
##    }
##        % else:
##    output.${gen_upper_camel(node.get_field_name())} = *ToDefine${node.get_name()}(input.${gen_upper_camel(node.get_field_name())})
##        % endif
##    % endfor
##    return &output
##}
##
##% elif st.is_resp():
##func ToGraphqlDefine${st.get_name()}(input *define.${st.get_name()}) (*${st.get_name()}) {
##    output := ${st.get_name()}{}
##    if input == nil {
##        return &output
##    }
##    % for field in st.fields():
##    output.${gen_upper_camel(field.get_name())} = input.${gen_upper_camel(field.get_name())}
##    % endfor
##    % for node in st.get_nodes():
##        % if type(node) == list:
##    for _, arg := range(input.${gen_upper_camel(node[0].get_field_name())}) {
##        output.${gen_upper_camel(node[0].get_field_name())} = append(output.${gen_upper_camel(node[0].get_field_name())}, *ToGraphqlDefine${node[0].get_name()}(&arg))
##    }
##        % else:
##    output.${gen_upper_camel(node.get_field_name())} = *ToGraphqlDefine${node.get_name()}(&input.${gen_upper_camel(node.get_field_name())})
##        % endif
##    % endfor
##    return &output
##}
##
##% endif
