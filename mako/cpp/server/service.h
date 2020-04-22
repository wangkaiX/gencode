#pragma once

#include "common/common_api.h"

template <typename Adapt, typename Connection>
class ${service_class_name}Impl : public CommonApi
{
public:
    % for api in framework.client_apis:
        % if framework.no_resp:
    void ${api.name}(const ${api.req.type.name} &req)
    {

    }
        % endif
    % endfor
private:
};

template <typename Adapt, typename Connection>
class ${service_class_name} : public ${service_class_name}Impl
{
public:
    ${service_class_name}(const std::string &host, unsigned short port)
        : _host(host)
        , _port(port)
    {
    }

private:
    std::string _host;
    unsigned short _port;
};
