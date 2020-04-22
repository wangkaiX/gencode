#include "common/common_api.h"

% for api in framework.client_apis:
    % if framework.no_resp:
void CommonApi::${api.name}(const ${api.req.type.name} &req)
    % else:
${api.resp.type.name} CommonApi::${api.name}(const ${api.req.type.name} &req)
    % endif
{
    assert(false && "请在基类中实现${api.name}" && __FUNCTION__);
}

% endfor
