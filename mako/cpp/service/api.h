#pragma once

#include <memory>
#include <map>
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
        init();
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
    std::map<CommandType, std::function<nlohmann::json (const nlohmann::json&)>> _callbacks;
private:
    void init()
    {
        % for api in framework.server_apis:
        _callbacks[${api.command_code}] = std::bind(&${framework.adapt_class_name}::${api.name}, this, std::placeholders::_1);
        % endfor

        % if len(framework.server_apis) > 0:
        _adapt_ptr->set_callback(std::bind(&${framework.service_class_name}Api::receive_callback, this, std::placeholders::_1));
        % endif
    }

    % if framework.no_resp:
    void receive_callback(nlohmann::json &j)
    % else:
    nlohmann::json receive_callback(const nlohmann::json &j)
    {
        CommandType command = j["${framework.command_name}"];
        return _callbacks[command](j);
    }
    % endif

/*
    // 发送请求
    % for api in framework.client_apis:
    % if api.no_resp:
    void ${api.name}(const ${api.req.type.name} &req)
    % else:
    ${api.resp.type.name} ${api.name}(const ${api.req.type.name} &req)
    % endif
    {
        return _adapt_ptr->request(req);
    }
  
    % endfor
*/

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
