#pragma once
#include <nlohmann/json.hpp>
#include "http_client.h"

% for include_file in include_files:
#include "interface/${include_file}"
% endfor

namespace safehouse{
class ${module_name}
{
public:
    ${module_name}(const char *address, unsigned short port, const char *target)
        :client_(address, port, target)
        {}

% for interface_name, req, resp in services:
    ${resp.get_type()} send_${interface_name}(const struct ${req.get_type()} &request)
    {   
        nlohmann::json j = request;
        j["module_name"] = "${interface_name}";
        return nlohmann::json::parse(client_.send(j).body().c_str());
    }

% endfor

private:
    SHHttpClient client_;
};
} // safehouse
