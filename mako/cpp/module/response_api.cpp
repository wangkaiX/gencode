#include "${module.module_name}/api.h"


% if module.no_resp:
void ${module.module_class_impl_name}::${api.name}(const ${api.req.type.name} &req)
{
}
% else:
${api.resp.type.name} ${module.module_class_impl_name}::${api.name}(const ${api.req.type.name} &req)
{
    ${api.resp.type.name} resp{};

    return resp;
}
% endif
