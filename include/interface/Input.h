#pragma once
#include "interface/A.h"

#include <nlohmann/json.hpp>

namespace safehouse{
struct Input
{
    A a;
};

inline void to_json(nlohmann::json &j, const Input &obj)
{
    j = nlohmann::json{
        {"a", obj.a},
    };
}

inline void from_json(const nlohmann::json &j, Input &obj)
{
    if(j.find("a") != j.end()) j.at("a").get_to(obj.a);
}
} // safehouse
