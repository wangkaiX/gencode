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
    % if field.is_necessary() or st.is_resp():
        <%
            flag = ''
        %>
    % else:
        <%
            flag = '*'
        %>
    % endif
    % if field.get_type()._kind in [data_type.TypeEnum.enum, data_type.TypeEnum.list_enum]:
        <%
          _type = 'string'
        %>
    % else:
        <%
          _type = field.get_type()._go
        %>
    % endif
    % if field.is_list():
    ${gen_title_name(field.get_name())} ${flag}[]${_type} // ${field.get_comment()}
    % else:
    ${gen_title_name(field.get_name())} ${flag}${_type} // ${field.get_comment()}
    % endif

% endfor
% for node in st.get_nodes():
    % if (type(node) == list and node[0].is_resp()) or (type(node) != list and node.is_resp()):
        <%
            flag = ''
        %>
    % else:
        <%
            flag = '*'
        %>
    % endif

    % if type(node) == list:
    ${gen_title_name(node[0].get_name())} ${flag}[]${flag}${node[0].get_name()} // ${node[0].get_comment()}
    % else:
    ${gen_title_name(node.get_name())} ${flag}${node.get_name()} // ${node.get_comment()}
    % endif

% endfor
}
