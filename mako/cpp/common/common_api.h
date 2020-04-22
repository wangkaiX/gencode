#pragma once

#include "common/types.h"

class CommonApi
{
public:
    % for api in server_apis:
    ${api.resp.type.name} ${api.name}(const ${api.req.type.name} &req);
    % endfor

    % for api in client_apis:
        % if framework.no_resp:
    virtual void ${api.name}(const ${api.req.type.name} &req);
        % else:
    virtual ${api.resp.type.name} ${api.name}(const ${api.req.type.name} &req);
        % endif
    % endfor

private:
    // 发送请求

    

    // 处理请求
};
