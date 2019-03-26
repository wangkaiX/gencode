#pragma once
#include <nlohmann/json.hpp>
#include "http_client.h"

#include "interface/Input.h"
#include "interface/Output.h"

namespace safehouse{
class ProjectManagerClient
{
public:
    ProjectManagerClient(const char *address, unsigned short port, const char *target)
        :client_(address, port, target)
        {}

    Output send_test(const struct Input &request)
    {   
        nlohmann::json j = request;
        j["service_name"] = "test";
        return nlohmann::json::parse(client_.send(j).body().c_str());
    }


private:
    SHHttpClient client_;
};
} // safehouse
