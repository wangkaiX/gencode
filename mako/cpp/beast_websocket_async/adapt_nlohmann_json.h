#include <functional>
#include <map>
#include <boost/beast.hpp>
#include <nlohmann/json.hpp>

#include "types.h"
#include "service_api.h"

class AdaptWebosocketNlohmannJson
{
public:
    std::string request(const boost::beast::flat_buffer &buffer)
    {
        std::string msg(static_cast<const char*>(buffer.data().data()), buffer.size());
        auto json = nlohmann::json::parse(msg);
        int command = json["${framework.command_name}"];
        return _callbacks[command](json); 
    }
private:
    void init()
    {
        % for api in apis:
        _callbacks[${api.command_code}] = std::bind(&AdaptWebosocketNlohmannJson::${api.name}, this, std::placeholders::_1);
        % endfor
    }

    % for api in apis:
    nlohmann::json ${api.name}(const nlohmann::json &json)
    {
        return _api_server.${api.name}(json);
    }
    % endfor
private:
    ApiServer _api_server;
    % if isinstance(api.command_code, int):
    std::map<int, std::function<nlohmann::json (nlohmann::json)>> _callbacks;
    % elif isinstance(api.command_code, str):
    std::map<std::string, std::function<nlohmann::json (nlohmann::json)>> _callbacks;
    % else:
        <%
        print("不支持的类型" % type(api.command_code))
        assert False
        %>
    % endif

};

