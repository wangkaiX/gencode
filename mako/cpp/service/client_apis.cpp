#include "${framework.service_name}/api.h"

% for api in framework.client_apis:
    % if framework.no_resp:
void ${framework.service_class_name}Api::${api.name}(const ${api.req.type.name} &req)
    % else:
${api.resp.type.name} ${framework.service_class_name}Api::${api.name}(const ${api.req.type.name} &req)
    % endif
{
    return _adapt_ptr->request(req);
}

% endfor
