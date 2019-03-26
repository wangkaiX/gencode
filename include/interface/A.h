#pragma once
#include "string"

#include <nlohmann/json.hpp>

namespace safehouse{
struct A
{
    int b;
    std::string c;
};

inline void to_json(nlohmann::json &j, const A &obj)
{
    j = nlohmann::json{
        {"b", obj.b},
        {"c", obj.c},
    };
}

inline void from_json(const nlohmann::json &j, A &obj)
{
    if(j.find("b") != j.end()) j.at("b").get_to(obj.b);
    if(j.find("c") != j.end()) j.at("c").get_to(obj.c);
}
} // safehouse
