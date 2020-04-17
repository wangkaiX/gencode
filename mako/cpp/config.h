#pragma once
#include <string>
% for include in std_includes:
#include <${include}>
% endfor
#include <fstream>
#include <nlohmann/json.hpp>

% for node in nodes:
<%
    members = node.fields + node.nodes
    if len(members) == 0:
        continue
%>

struct ${node.type.cpp}
{
% for member in members:
    % if member.note:
    // ${member.note}
    % endif
    % if 1 == member.dimension:
    std::vector<${member.type.cpp}> ${member.name};
    % elif 0 == member.dimension:
    ${member.type.cpp} ${member.name};
    % else:
    <% 
       print("不支持多维数组")
       assert False
    %>
    % endif
% endfor
};

// inline void to_json(nlohmann::json &j, const ${node.type.name} &obj)
// {
//     j = nlohmann::json{
//         % for member in members:
//         {"${member.name}", obj.${member.name}},
//         % endfor
//     };
// }

<% from code_framework import framework %>

inline void from_json(const nlohmann::json &j, ${node.type.name} &obj)
{
% for member in members:
    if(j.find("${member.name}") == j.end()) {
        throw "缺少配置项[${member.name}]";
    }
    else {
        j.at("${member.name}").get_to(obj.${member.name});
        % if member.type.is_string: 
        if (obj.${member.name} == "") {
            throw "缺少配置项[${member.name}]";
        }
        % endif
    }
% endfor
}
% endfor

struct LoadConfig
{
public:
    LoadConfig(const std::string &filename)
    {
        std::ifstream ifs(filename);
        nlohmann::json j;
        ifs >> j;
        config = j;
    }
    Config config;

};

inline Config &getCfg()
{
    static LoadConfig load("config/config.json");
    return load.config;
}
