#pragma once
#include <string>
% for include in std_includes:
#include <${include}>
% endfor

% for enum in enums:
% if enum.base_type:
enum class ${enum.name} : ${enum.base_type}
% else:
enum class ${enum.name}
% endif
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
    % if member.fixed_size:
    ${member.type.cpp} ${member.name}[${member.fixed_size}];
    % else:
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
    % endif
% endfor
};

% endfor
