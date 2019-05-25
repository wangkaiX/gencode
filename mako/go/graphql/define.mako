package ${package}

import "${pro_path}/app/define"

% for field in st.fields():
    % if 'time.Time' == field.get_type()._go:
import "time"
        <% break %>
    % endif
% endfor
<%
from gencode_pkg.common import data_type
%>

// ${st.get_name()} ${st.get_comment()}
type  ${st.get_name()} struct {
% for field in st.fields():
    <%
    if field.is_necessary() or st.is_resp():
          flag = ''
    else:
          flag = '*'
    if field.get_type()._kind in [data_type.TypeEnum.enum, data_type.TypeEnum.list_enum]:
        _type = 'string'
    else:
        _type = field.get_type()._go
    %>
    % if field.is_list():
    ${gen_title_name(field.get_name())} ${flag}[]${_type} // ${field.get_comment()}
    % else:
    ${gen_title_name(field.get_name())} ${flag}${_type} // ${field.get_comment()}
    % endif

% endfor
% for node in st.get_nodes():
    <%
    if (type(node) == list and node[0].is_resp()) or (type(node) != list and node.is_resp()):
          flag = ''
    else:
          flag = '*'
    %>
    % if type(node) == list:
    ${gen_title_name(node[0].get_field_name())} ${flag}[]${flag}${node[0].get_name()} // ${node[0].get_comment()}
    % else:
    ${gen_title_name(node.get_field_name())} ${flag}${node.get_name()} // ${node.get_comment()}
    % endif

% endfor
}

% if st.is_req():
func ToDefine${st.get_name()}(input *${st.get_name()}) (*define.${st.get_name()}) {
    output := define.${st.get_name()}{}
    if input == nil {
        return &output
    }
    % for field in st.fields():
        % if not field.is_necessary():
    if input.${gen_title_name(field.get_name())} != nil {
        output.${gen_title_name(field.get_name())} = *input.${gen_title_name(field.get_name())}
    }
        % else:
    output.${gen_title_name(field.get_name())} = input.${gen_title_name(field.get_name())}
        % endif
    % endfor
    % for node in st.get_nodes():
        % if type(node) == list:
    if input.${gen_title_name(node[0].get_field_name())} != nil {
        for _, arg := range(*input.${gen_title_name(node[0].get_field_name())}) {
            output.${gen_title_name(node[0].get_field_name())} = append(output.${gen_title_name(node[0].get_field_name())}, *ToDefine${node[0].get_name()}(arg))
        }
    }
        % else:
    output.${gen_title_name(node.get_field_name())} = *ToDefine${node.get_name()}(input.${gen_title_name(node.get_field_name())})
        % endif
    % endfor
    return &output
}

% elif st.is_resp():
func ToGraphqlDefine${st.get_name()}(input *define.${st.get_name()}) (*${st.get_name()}) {
    output := ${st.get_name()}{}
    if input == nil {
        return &output
    }
    % for field in st.fields():
    output.${gen_title_name(field.get_name())} = input.${gen_title_name(field.get_name())}
    % endfor
    % for node in st.get_nodes():
        % if type(node) == list:
    for _, arg := range(input.${gen_title_name(node[0].get_field_name())}) {
        output.${gen_title_name(node[0].get_field_name())} = append(output.${gen_title_name(node[0].get_field_name())}, *ToGraphqlDefine${node[0].get_name()}(&arg))
    }
        % else:
    output.${gen_title_name(node.get_field_name())} = *ToGraphqlDefine${node.get_name()}(&input.${gen_title_name(node.get_field_name())})
        % endif
    % endfor
    return &output
}

% endif
