#include "${module.module_name}/api.h"

% for api in module.request_apis:
    % if module.no_resp:
void ${module.module_class_impl_name}::${api.name}(const ${api.req.type.name} &req)
    % else:
${api.resp.type.name} ${module.module_class_impl_name}::${api.name}(const ${api.req.type.name} &req)
    % endif
{
    return request(req);
}

% endfor
