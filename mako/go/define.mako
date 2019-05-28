package define

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
    if field.get_type()._kind in [data_type.TypeEnum.enum, data_type.TypeEnum.list_enum]:
        _type = 'string'
    else:
        _type = field.get_type()._go
    if field.is_list():
        _type = '[]' + _type
    if st.is_req() and field.is_necessary():
        required = ' binding:"required"'
    else:
        required = ''
    %>
    ${gen_title_name(field.get_name())} ${_type} `json:"${field.get_name()}"${required}`// ${field.get_comment()}

% endfor
% for node in st.get_nodes():
    <% required = '' %>
    % if type(node) == list:
    <%
        if node[0].is_necessary():
            required = ' binding:"required"'
    %>
    ${gen_title_name(node[0].get_field_name())} []${node[0].get_name()} `json:"${node[0].get_field_name()}"${required}` // ${node[0].get_comment()}
    % else:
    <%
        if node.is_necessary():
            required = ' binding:"required"'
    %>
    ${gen_title_name(node.get_field_name())} ${node.get_name()} `json:"${node.get_field_name()}"${required}` // ${node.get_comment()}
    % endif

% endfor
}
