#pragma once

#include <memory>
#include "${framework.service_name}/types.h"
#include "${framework.service_name}/${framework.adapt_name}.h"
% for include in include_list:
#include "${include}"
% endfor

class ${framework.service_class_name}Api
{
public:
    ${framework.service_class_name}Api(boost::asio::io_context &io_context, const boost::asio::ip::tcp::endpoint &ep)
        : _adapt_ptr(std::make_shared<${framework.adapt_class_name}<${connection_class_name}>>(io_context, ep))
    {
    }
    // 处理请求
    % for api in framework.server_apis:
    ${api.resp.type.name} ${api.name}(const ${api.req.type.name} &req);
    % endfor

    // 发送请求
    % for api in framework.client_apis:
        % if api.no_resp:
    void ${api.name}(const ${api.req.type.name} &req);
        % else:
    ${api.resp.type.name} ${api.name}(const ${api.req.type.name} &req);
        % endif
    % endfor

private:
    std::shared_ptr<${framework.adapt_class_name}<${connection_class_name}>> _adapt_ptr;

};
