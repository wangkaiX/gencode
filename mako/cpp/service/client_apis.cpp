#include "${framework.service_name}/api.h"

% for api in framework.client_apis:
    % if framework.no_resp:
void ${framework.service_api_class_name}::${api.name}(const ${api.req.type.name} &req)
    % else:
${api.resp.type.name} ${framework.service_api_class_name}::${api.name}(const ${api.req.type.name} &req)
    % endif
{
    return _adapt_ptr->request(req);
}

% endfor
