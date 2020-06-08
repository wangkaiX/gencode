#include "${module.module_name}/api.h"


% if module.no_resp:
void ${module.service_api_class_name}::${api.name}(const ${api.req.type.name} &req)
{
}
% else:
${api.resp.type.name} ${module.service_api_class_name}::${api.name}(const ${api.req.type.name} &req)
{
    ${api.resp.type.name} resp{};

    return resp;
}
% endif
