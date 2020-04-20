#pragma once

#include "types.h"

class ${service_class_name}
{
public:
    % for api in server_apis:
    ${api.resp.type.name} ${api.name}(const ${api.req.type.name} &req);
    % endfor

    % for api in client_apis:
    ${api.resp.type.name} ${api.name}(const ${api.req.type.name} &req);
    % endfor
private:
    // 发送请求

    

    // 处理请求
};
