#include "${framework.service_name}/api.h"

${framework.service_api_class_name}::${framework.service_api_class_name}(boost::asio::io_context &io_context, std::shared_ptr<${connection_class_name}> connection_ptr)
    : _adapt_ptr(std::make_shared<${framework.adapt_class_name}<${connection_class_name}>>(io_context, connection_ptr))
{
    init();
}


void ${framework.service_api_class_name}::init()
{
    % for api in framework.server_apis:
    _callbacks[${api.command_code}] = std::bind(static_cast<MemberCallbackType>(&${framework.service_api_class_name}::${api.name}), this->shared_from_this(), std::placeholders::_1);
    % endfor

    % if len(framework.server_apis) > 0:
    _adapt_ptr->set_callback(std::bind(&${framework.service_api_class_name}::receive_callback, this->shared_from_this(), std::placeholders::_1));
    % endif
}

% if framework.no_resp:
void ${framework.service_api_class_name}::receive_callback(const nlohmann::json &j)
% else:
nlohmann::json ${framework.service_api_class_name}::receive_callback(const nlohmann::json &j)
% endif
{
    CommandType command = j["${framework.command_name}"];
    return _callbacks[command](j);
}

// 处理请求
% for api in framework.server_apis:
% if framework.no_resp:
void ${framework.service_api_class_name}::${api.name}(const nlohmann::json &json)
% else:
nlohmann::json ${framework.service_api_class_name}::${api.name}(const nlohmann::json &json)
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
