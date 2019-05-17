package resolver

import "${pro_path}/app/define"

% for field in resp.fields():
    % if 'time' == field.get_type()._type:
import graphql "github.com/graph-gophers/graphql-go"
import "time"
        <% break %>
    % endif
% endfor

type ${resp.get_name()}Resolver struct {
    r *define.${resp.get_name()}
}

% for field in resp.fields():
    % if field.is_list():
func (r *${get_resolver_type(resp.get_name())}) ${gen_title_name(field.get_name())}() ${get_resolver_rettype(field)} {
    ${field.get_name()}Resolver := ${get_list_type(field)}{}
    for _, v := range r.r.${gen_title_name(field.get_name())} {
        t := ${get_resolver_type(field.get_type())}{${get_addr_op(field)}v}
        ${field.get_name()}Resolver = append(${field.get_name()}Resolver, ${get_addr_op(field)}t)
    }
    return ${get_addr_op(field)}${field.get_name()}Resolver
    % elif field.is_object():
func (r *${get_resolver_type(resp.get_name())}) ${gen_title_name(field.get_name())}() *${get_resolver_rettype(field)} {
    return &${get_resolver_rettype(field)}{${get_addr_op(field)}r.r.${gen_title_name(field.get_name())}}
    % else:
func (r *${get_resolver_type(resp.get_name())}) ${gen_title_name(field.get_name())}() ${get_resolver_rettype(field)} {
        % if field.get_type()._type == 'time':
    return ${get_resolver_rettype(field)}{${get_addr_op(field)}r.r.${gen_title_name(field.get_name())}}
        % else:
    return r.r.${gen_title_name(field.get_name())}
        % endif
    % endif
}
% endfor
