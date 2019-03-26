#pragma once
#include "string"

#include <nlohmann/json.hpp>

namespace safehouse{
struct Output
{
    std::string a2;
    // 错误码
    std::string error_code;
    // 错误信息
    std::string error_msg;
};

inline void to_json(nlohmann::json &j, const Output &obj)
{
    j = nlohmann::json{
        {"a2", obj.a2},
        {"error_code", obj.error_code},
        {"error_msg", obj.error_msg},
    };
}

inline void from_json(const nlohmann::json &j, Output &obj)
{
    if(j.find("a2") != j.end()) j.at("a2").get_to(obj.a2);
    if(j.find("error_code") == j.end()) {
        throw "缺少参数[error_code]";
    }
    j.at("error_code").get_to(obj.error_code);
    if(j.find("error_msg") == j.end()) {
        throw "缺少参数[error_msg]";
    }
    j.at("error_msg").get_to(obj.error_msg);
}
} // safehouse
