#include <functional>
#include <map>
#include <boost/beast.hpp>
#include <nlohmann/json.hpp>
#include <iostream>

#include "api/types.h"
#include "api/api.h"

class ${framework.adapt_class_name}
{
public:
    ${framework.adapt_class_name}()
    {   
        init();
    }
    std::string request(const boost::beast::flat_buffer &buffer)
    {
        try {
            std::string msg(static_cast<const char*>(buffer.data().data()), buffer.size());
            auto json = nlohmann::json::parse(msg);
            int command = json["${framework.command_name}"];
            return _callbacks[command](json).dump();
        }
        catch (std::exception &e) {
            nlohmann::json j;
            j["code"] = -1; 
            j["msg"] = "解析接口类型失败";
            std::cout << j.dump(4) << std::endl;
            return j.dump();
        }
    }
private:
    void init()
    {
        % for api in apis:
        _callbacks[${api.command_code}] = std::bind(&${framework.adapt_class_name}::${api.name}, this, std::placeholders::_1);
        % endfor
    }

    % for api in apis:
    nlohmann::json ${api.name}(const nlohmann::json &json)
    {
        try {
            return _api_server.${api.name}(json);
        }
        catch (std::exception &e) {
            ${api.resp.type.name} resp{};
            resp.code = -1;
            resp.msg = e.what();
            std::cout << e.what() << std::endl;
        }
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

