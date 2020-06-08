#include "${module.module_name}/api.h"

% for api in module.request_apis:
    % if module.no_resp:
void ${module.service_api_class_name}::${api.name}(const ${api.req.type.name} &req)
    % else:
${api.resp.type.name} ${module.service_api_class_name}::${api.name}(const ${api.req.type.name} &req)
    % endif
{
    return request(req);
}

% endfor
