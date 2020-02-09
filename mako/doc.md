% for i, api in zip(range(1, len(apis)+1), apis):
# ${i}、${api.note}
<%
    req = api.req
    resp = api.resp
%>

请求地址
```
${api.gw_url}
```

请求方法:
```
${api.method}
```

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

${field_list(api.cookie, "cookie:(*为必填项)")}

${field_list(api.url_param, "URL参数:(*为必填项)")}

${field_list(api.context, "HEAD参数:(*为必填项)")}

% if req and (len(req.fields) + len(req.nodes)) > 0:
请求参数:(*为必填项)
|名称|类型|描述|
|----|----|----|
% for field in req.fields + nodes2fields(req.nodes):
|${markdown_full_path(field.full_path)}${"*" if field.required else ""}|${markdown_type(enums, field)}|${markdown_note(enums, field)}|
% endfor
% endif

% if resp.has_file:
文件下载成功的情况：
Content-Type: application/octet-stream
body中为文件
http返回状态码：200

文件下载失败的情况：
Content-Type: application/json
body中为json字符串
http返回状态码：404
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

<%
    input_text = dict2json(req.value_map)
    output_text = dict2json(resp.value_map)
%>
请求示例:
<% 
    cookies = ''
    if api.cookie:
        for cookie in api.cookie.fields:
            cookies += "%s=%s;" % (cookie.name, cookie.value)
    if cookies:
        cookies = cookies[:-1]
    url_param = ''
    if api.url_param:
        url_param = url_param2text(api.url_param.fields)
%>
```
curl -X ${api.method} \
http://ip:port${api.gw_url}${url_param} \
-H 'Content-Type: application/json' \
% if api.context:
    % for ctx in api.context.fields:
-H '${ctx.name}: ${ctx.value}'
    % endfor
% endif
% if cookies:
--cookie '${cookies}'
% endif
-d '
   ${input_text}
'
```

应答示例:
```
${output_text}
```

% endfor

错误码说明
% if errnos and len(errnos) > 0:
|errno_code|error_msg|errno_no|
|----|----|----|
% for errno in errnos:
|${errno.code}|${errno.msg}|${errno.no}|
% endfor
% endif
