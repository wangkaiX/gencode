#pragma once
% for include_file in include_files:
#include "${include_file}"
% endfor

#include <nlohmann/json.hpp>

namespace safehouse{
struct ${class_name}
{
% for field in fields:
    % if field.get_comment():
    // ${field.get_comment()}
    % endif
    ${field.get_type()._cpp} ${field.get_name()};
% endfor
};

inline void to_json(nlohmann::json &j, const ${class_name} &obj)
{
    j = nlohmann::json{
        % for field in fields:
        {"${field.get_name()}", obj.${field.get_name()}},
        % endfor
    };
}

inline void from_json(const nlohmann::json &j, ${class_name} &obj)
{
% for field in fields:
    % if field.is_necessary():
    if(j.find("${field.get_name()}") == j.end()) {
        throw "缺少参数[${field.get_name()}]";
    }
    j.at("${field.get_name()}").get_to(obj.${field.get_name()});
    % if field.is_string():
    if (obj.${field.get_name()} == "") {
        throw "缺少参数[${field.get_name()}]";
    }
    % endif
    % else:
    if(j.find("${field.get_name()}") != j.end()) j.at("${field.get_name()}").get_to(obj.${field.get_name()});
    % endif
% endfor
}
} // safehouse
