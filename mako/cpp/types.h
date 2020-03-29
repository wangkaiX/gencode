#pragma once
#include <string>
% for include in std_includes:
#include <${include}>
% endfor

#include <nlohmann/json.hpp>

% for enum in enums:
enum class ${enum.name}
{
    % for value in enum.values:
    // ${value.note}
    ${value.value},
    % endfor
};
% endfor

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

inline void to_json(nlohmann::json &j, const ${node.type.name} &obj)
{
    j = nlohmann::json{
        % for member in members:
        {"${member.name}", obj.${member.name}},
        % endfor
    };
}

<% from code_framework import framework %>

inline void from_json(const nlohmann::json &j, ${node.type.name} &obj)
{
    std::string less_fields;
% for member in members:
    % if member.required:
    if(j.find("${member.name}") == j.end()) {
        less_fields += "[${member.name}]";
    }
    else {
        % if isinstance(member, framework.Node):
        try {
            j.at("${member.name}").get_to(obj.${member.name});
        }
        catch (std::string &e) {
            less_fields += e;
        }
        % elif member.type.is_string:
        if (obj.${member.name} == "") {
            less_fields += "[${member.name}]";
        }
        % else:
        j.at("${member.name}").get_to(obj.${member.name});
        % endif
    }
    % else:
    if(j.find("${member.name}") != j.end()) j.at("${member.name}").get_to(obj.${member.name});
    % endif
% endfor
    if (less_fields.size() > 0) {
        throw "缺少参数" + less_fields;
    }
}

% endfor
