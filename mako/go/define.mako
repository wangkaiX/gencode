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
        _type = 'int32'
    else:
        _type = field.get_type()._go
    %>
    % if field.is_list():
    ${gen_title_name(field.get_name())} []${_type} // ${field.get_comment()}
    % else:
    ${gen_title_name(field.get_name())} ${_type} // ${field.get_comment()}
    % endif

% endfor
% for node in st.get_nodes():
    % if type(node) == list:
    ${gen_title_name(node[0].get_field_name())} []${node[0].get_name()} // ${node[0].get_comment()}
    % else:
    ${gen_title_name(node.get_field_name())} ${node.get_name()} // ${node.get_comment()}
    % endif

% endfor
}
