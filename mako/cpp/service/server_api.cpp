#include "${framework.service_name}/api.h"


% if framework.no_resp:
void ${framework.service_api_class_name}::${api.name}(const ${api.req.type.name} &req)
{
}
% else:
${api.resp.type.name} ${framework.service_api_class_name}::${api.name}(const ${api.req.type.name} &req)
{
    ${api.resp.type.name} resp{};

    return resp;
}
% endif
