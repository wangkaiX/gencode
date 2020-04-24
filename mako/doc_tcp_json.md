% for i, api in zip(range(1, len(apis)+1), apis):
# ${i}、${api.note}
<%
    req = api.req
    resp = api.resp
%>

<%def name="field_list(block, block_name)">
% if block and len(block.fields) > 0:
${block_name}:
|名称|类型|描述|
|----|----|----|
% for field in block.fields:
|${field.name}${"*" if field.required else ""}|${markdown_type(enums, field)}|${markdown_note(enums, field)}|
% endfor
% endif

</%def>

% if req and (len(req.fields) + len(req.nodes)) > 0:
请求参数:(*为必填项)
|名称|类型|描述|
|----|----|----|
% for field in req.fields + nodes2fields(req.nodes):
|${markdown_full_path(field.full_path)}${"*" if field.required else ""}|${markdown_type(enums, field)}|${markdown_note(enums, field)}|
% endfor
% endif

应答参数:
|名称|类型|描述|
|----|----|----|
% for field in resp.fields + nodes2fields(resp.nodes):
    % if field.type.is_file:
      <% 
        continue
      %>
    % endif
|${markdown_full_path(field.full_path)}|${markdown_type(enums, field)}|${markdown_note(enums, field)}|
% endfor

% endfor

错误码说明
% if errnos and len(errnos) > 0:
|errno_code|error_msg|errno_no|
|----|----|----|
% for errno in errnos:
|${errno.code}|${errno.msg}|${errno.no}|
% endfor
% endif
