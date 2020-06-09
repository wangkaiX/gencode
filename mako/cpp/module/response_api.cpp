#include "${module.name}/api.h"


% if module.no_resp:
void ${module.class_impl_name}::${api.name}(const ${api.req.type.name} &req)
{
}
% else:
${api.resp.type.name} ${module.class_impl_name}::${api.name}(const ${api.req.type.name} &req)
{
    ${api.resp.type.name} resp{};

    return resp;
}
% endif
