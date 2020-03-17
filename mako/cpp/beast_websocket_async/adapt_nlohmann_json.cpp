#include <functional>
#include <boost/beast.hpp>
#include <nlohmann/json.hpp>

#include "types.h"
#include "task_manager.h"

class AdaptNlohmannJson
{
public:
    std::string request(const boost::beast::flat_buffer &buffer)
    {
        std::string msg(static_cast<const char*>(buffer.data().data()), buffer.size());
        auto json = nlohmann::json::parse(msg);
        int command = json["type"];
        _callbacks[command](json); 
    }
private:
    void init()
    {
        % for api in apis:
        _callbacks[${api.command_code}] = std::bind(&AdaptNlohmannJson::${api.name}, this, std::placeholders::_1);
        % endfor
    }

    % for api in apis:
    nlohmann::json ${api.name}(const nlohmann::json &json)
    {
        return _task_manager.${api.name}(json);
    }
    % endfor
private:
    TaskManager _task_manager;
    std::map<int, std::function<nlohmann::json (nlohmann::json)>> _callbacks;
};

