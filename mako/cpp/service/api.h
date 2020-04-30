#pragma once

#include <memory>
#include <map>
#include "${framework.service_name}/types.h"
#include "${framework.service_name}/${framework.adapt_name}.h"
% for include in include_list:
#include "${include}"
% endfor

class ${framework.service_api_class_name}: public std::enable_shared_from_this<${framework.service_api_class_name}>
{
public:
    ${framework.service_api_class_name}(boost::asio::io_context &io_context, std::shared_ptr<${connection_class_name}> connection_ptr);

    void init();
    // 处理请求
    % for api in framework.server_apis:
    % if framework.no_resp:
    void ${api.name}(const ${api.req.type.name} &req);
    % else:
    ${api.resp.type.name} ${api.name}(const ${api.req.type.name} &req);
    % endif
    % endfor

    // 发送请求
    % for api in framework.client_apis:
        % if framework.no_resp:
    void ${api.name}(const ${api.req.type.name} &req);
        % else:
    ${api.resp.type.name} ${api.name}(const ${api.req.type.name} &req);
        % endif
    % endfor

private:
    std::shared_ptr<${framework.adapt_class_name}<${connection_class_name}>> _adapt_ptr;
    // ${framework.adapt_class_name}

    % if isinstance(api.command_code, int):
    using CommandType = int;
    % elif isinstance(api.command_code, str):
    using CommandType = std::string;
    % else:
        <%  
        print("不支持的类型" % type(api.command_code))
        assert False
        %>  
    % endif
    % if framework.no_resp:
    using CallbackType = std::function<void(const nlohmann::json&)>;
    using MemberCallbackType = void (${framework.service_api_class_name}::*)(const nlohmann::json&);
    % else:
    using CallbackType = std::function<nlohmann::json (const nlohmann::json&)>;
    using MemberCallbackType = nlohmann::json (${framework.service_api_class_name}::*)(const nlohmann::json&);
    % endif
    std::map<CommandType, CallbackType> _callbacks;
private:

    % if framework.no_resp:
    void receive_callback(const nlohmann::json &j);
    % else:
    nlohmann::json receive_callback(const nlohmann::json &j);
    % endif

    // 处理请求
    % for api in framework.server_apis:
        % if framework.no_resp:
    void ${api.name}(const nlohmann::json &json);
        % else:
    nlohmann::json ${api.name}(const nlohmann::json &json);
        % endif
    % endfor
};
