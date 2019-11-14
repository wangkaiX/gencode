% for i, api in zip(range(1, len(apis)+1), apis):
# ${i}、${api.note}

请求地址
```
${api.gw_url}
```

请求方法:
```
${api.method}
```

% if api.cookie and len(api.cookie.fields) > 0:
cookie:
|名称|类型|描述|
|----|----|----|
% for field in api.cookie.fields:
|${field.name}${"*" if field.required else ""}|${"Enum" if is_enum(enum_names, field.type) else field.type.name}|${field.note}|
% endfor
% endif

% if api.url_param and len(api.url_param.fields) > 0:
URL参数:(*为必填项)
|名称|类型|描述|
|----|----|----|
% for field in api.url_param.fields:
|${field.name}${"*" if field.required else ""}|${"Enum" if is_enum(enum_names, field.type) else field.type.name}|${field.note}|
% endfor
% endif

% if api.context and len(api.context.fields) > 0:
HEAD参数:
|名称|类型|描述|
|----|----|----|
% for field in api.context.fields:
% if field.name in ('x-uid', 'X-UID'):
<% continue %>
% endif
|${field.name}${"*" if field.required else ""}|${"Enum" if is_enum(enum_names, field.type) else field.type.name}|${field.note}|
% endfor
% endif


% if api.req and len(api.req.fields) > 0:
请求参数:(*为必填项)
|名称|类型|描述|
|----|----|----|
% for field in api.req.fields + api.req.nodes:
|${markdown_full_path(field.full_path)}${"*" if field.required else ""}|${"Enum" if is_enum(enum_names, field.type) else field.type.name}|${field.note}|
% endfor
% endif

应答参数:
|名称|类型|描述|
|----|----|----|
% for field in api.resp.fields:
|${markdown_full_path(field.full_path)}|${"Enum" if is_enum(enum_names, field.type) else field.type.name}|${field.note}|
% endfor

<%
    input_text = dict2json(api.req.value_map)
    output_text = dict2json(api.resp.value_map)
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
--cookie '${cookies}'
-d '
   ${input_text}
'
```

应答示例:
```
${output_text}
```

% endfor
