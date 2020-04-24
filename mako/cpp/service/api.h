#pragma once

#include <memory>
#include <map>
#include "${framework.service_name}/types.h"
#include "${framework.service_name}/${framework.adapt_name}.h"
% for include in include_list:
#include "${include}"
% endfor

class ${framework.service_class_name}: public std::enable_shared_from_this<${framework.service_class_name}>
{
public:
    ${framework.service_class_name}(boost::asio::io_context &io_context, const boost::asio::ip::tcp::endpoint &ep)
        : _adapt_ptr(std::make_shared<${framework.adapt_class_name}<${connection_class_name}>>(io_context, ep))
    {
        init();
    }
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
    using MemberCallbackType = void (${framework.service_class_name}::*)(const nlohmann::json&);
    % else:
    using CallbackType = std::function<nlohmann::json (const nlohmann::json&)>;
    using MemberCallbackType = nlohmann::json (${framework.service_class_name}::*)(const nlohmann::json&);
    % endif
    std::map<CommandType, CallbackType> _callbacks;
private:
    void init()
    {
        % for api in framework.server_apis:
        _callbacks[${api.command_code}] = std::bind(static_cast<MemberCallbackType>(&${framework.service_class_name}::${api.name}), this->shared_from_this(), std::placeholders::_1);
        % endfor

        % if len(framework.server_apis) > 0:
        _adapt_ptr->set_callback(std::bind(&${framework.service_class_name}::receive_callback, this->shared_from_this(), std::placeholders::_1));
        % endif
    }

    % if framework.no_resp:
    void receive_callback(const nlohmann::json &j);
    % else:
    nlohmann::json receive_callback(const nlohmann::json &j)
    {
        CommandType command = j["${framework.command_name}"];
        return _callbacks[command](j);
    }
    % endif

    // 处理请求
    % for api in framework.server_apis:
    % if framework.no_resp:
    void ${api.name}(const nlohmann::json &json)
    % else:
    nlohmann::json ${api.name}(const nlohmann::json &json)
    % endif
    {
        try {
            ${api.req.type.name} req = json;
            return ${api.name}(req);
        }
        catch (std::exception &e) {
            % if framework.no_resp:
            SPDLOG_ERROR("[{}]", e.what());
            % else:
            ${api.resp.type.name} resp{};
            resp.code = -1;
            resp.msg = e.what();
            SPDLOG_ERROR("[{}]", e.what());
            return resp;
            % endif
        }
    }
  
    % endfor
};
