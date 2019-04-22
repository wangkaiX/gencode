package resolver

import "git.ucloudadmin.com/securehouse/dataflow/dataviewer/app/define"
% for field in resp.fields():
    % if 'time' == field.get_type()._type:
import graphql "github.com/graph-gophers/graphql-go"
        <% break %>
    % endif
% endfor

type ${resp.get_type()}Resolver struct {
    r *define.${resp.get_type()}
}

% for field in resp.fields():
    % if field.is_list():
func (r *${get_resolver_type(resp.get_type())}) ${gen_title_name(field.get_name())}() ${get_resolver_rettype(field)} {
    ${field.get_name()}Resolver := ${get_list_type(field)}{}
    for _, v := range r.r.${gen_title_name(field.get_name())} {
        t := ${get_resolver_type(field.get_base_type())}{${get_addr_op(field)}v}
        ${field.get_name()}Resolver = append(${field.get_name()}Resolver, ${get_addr_op(field)}t)
    }
    return ${get_addr_op(field)}${field.get_name()}Resolver
    % else:
func (r *${get_resolver_type(resp.get_type())}) ${gen_title_name(field.get_name())}() ${get_resolver_rettype(field)} {
        % if field.is_object() or field.get_type()._type == 'time':
    return ${get_resolver_rettype(field)}{${get_addr_op(field)}r.r.${gen_title_name(field.get_name())}}
        % elif field.get_type()._type == 'time':
        % else:
    return r.r.${gen_title_name(field.get_name())}
        % endif
    % endif
}
% endfor
