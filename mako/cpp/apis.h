#pragma once

#include "types.h"

class ApiServer
{
public:
    % for api in apis:
    ${api.resp.type.name} ${api.name}(const ${api.req.type.name} &req);
    % endfor
};
