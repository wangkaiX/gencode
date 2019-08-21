<% import os %>
package ${os.path.basename(restful_define_dir)}

% for field in node.fields:
    % if field.type.basename == 'GINFILE':
import "mime/multipart"
       <% break %>
    % endif
% endfor

% for field in node.fields:
    % if 'time' == field.type.basename:
import "time"
        <% break %>
    % endif
% endfor
<%
from gencode.common import meta
%>

// ${node.type.name} ${node.note}
type  ${node.type.name} struct {
% for field in node.fields + node.nodes:
    <%
    _type = '[]' * field.dimension + field.type.name
    if node.attr.is_req and field.required:
        required = ' binding:"required"'
    else:
        required = ''
    %>
    ${gen_upper_camel(field.name)} ${_type} `form:"${field.name}" json:"${field.name}"${required}`// ${field.note}

% endfor

}
