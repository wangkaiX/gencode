% for i, api in zip(range(1, len(apis)+1), apis):
# ${i}、${api.note}

请求地址
```
${api.url}
```

请求方法:
```
${api.method}
```

% if len(api.cookie.fields) > 0:
cookie:(*为必填项, 如果不走网关则cookie不需要)
|名称|类型|描述|
|----|----|----|
% for field in api.cookie.fields:
|${field.name}${"*" if field.required else ""}|${"Enum" if field.type.is_enum else field.type.name}|${field.note}|
% endfor
% endif

% if len(api.url_param.fields) > 0:
URL参数:(*为必填项)
|名称|类型|描述|
|----|----|----|
% for field in api.url_param.fields:
|${field.name}${"*" if field.required else ""}|${"Enum" if field.type.is_enum else field.type.name}|${field.note}|
% endfor
% endif

% if len(api.context.fields) > 0:
HEAD参数:(*为必填项, 如果走网关则head不需要)
|名称|类型|描述|
|----|----|----|
% for field in api.context.fields:
|${field.name}${"*" if field.required else ""}|${"Enum" if field.type.is_enum else field.type.name}|${field.note}|
% endfor
% endif


% if len(api.req_md_fields()) > 0:
请求参数:(*为必填项)
|名称|类型|描述|
|----|----|----|
% for field in api.req_md_fields():
|${field.md_full_path}${"*" if field.required else ""}|${"Enum" if field.type.is_enum else field.type.name}|${field.note}|
% endfor
% endif

应答参数:
|名称|类型|描述|
|----|----|----|
% for field in api.resp_md_fields():
|${field.md_full_path}|${"Enum" if field.type.is_enum else field.type.name}|${field.note}|
% endfor

<%
    json_input = dict2json(api.req.value)
    json_output = dict2json(api.resp.value)
%>
请求示例:
<% 
    cookies = ''
    for cookie in api.cookie.fields:
        cookies += "%s=%s;" % (cookie.name, cookie.value)
    if cookies:
        cookies = cookies[:-1]
%>
```
curl -X ${api.method} \
http://ip:port${api.url}${api.url_param.url_param} \
-H 'Content-Type: application/json' \
% for ctx in api.context.fields:
-H '${ctx.name}: ${ctx.value}'
% endfor
--cookie '${cookies}'
-d '
   ${json_input}
'
```

应答示例:
```
${json_output}
```

% endfor
