#pragma once
#include <string>
% for include in std_includes:
#include <${include}>
% endfor

#include <nlohmann/json.hpp>
<% nodes.reverse() %>

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
    ${member.type.cpp} ${member.name};
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

inline void from_json(const nlohmann::json &j, ${node.type.name} &obj)
{
    std::string less_fields;
% for member in members:
    % if member.required:
    if(j.find("${member.name}") == j.end()) {
        less_fields += "[${member.name}]";
    }
    else {
        j.at("${member.name}").get_to(obj.${member.name});
    }
        % if member.type.is_string:
    if (obj.${member.name} == "") {
        less_fields += "[${member.name}]";
    }
        % endif
    % else:
    if(j.find("${member.name}") != j.end()) j.at("${member.name}").get_to(obj.${member.name});
    % endif
% endfor
}

% endfor
