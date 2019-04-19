package resolver

import "git.ucloudadmin.com/securehouse/dataflow/dataviewer/app/define"
% for field in resp.fields():
    % if 'time.Time' == field.get_type()._type_go:
import graphql "github.com/graph-gophers/graphql-go"
        <% break %>
    % endif
% endfor

type ${resp.get_type()}Resolver struct {
    r *define.${resp.get_type()}
}

% for field in resp.fields():
    % if field.get_type()._type == 'time':
func (r *${resp.get_type()}Resolver) ${gen_title_name(field.get_name())}() graphql.Time {
    return graphql.Time{r.r.${gen_title_name(field.get_name())}}
    % elif field.is_list():
        % if field.is_object():
func (r *${resp.get_type()}Resolver) ${gen_title_name(field.get_name())}() *[]*${field.get_base_type()}Resolver{
    ${field.get_name()}Resolver := []*${field.get_base_type()}Resolver{}
    for _, v := range r.r.${gen_title_name(field.get_name())} {
        t := ${field.get_base_type()}Resolver{&v}
        ${field.get_name()}Resolver = append(${field.get_name()}Resolver, &t)
    }
    return &${field.get_name()}Resolver
        % else:
func (r *${resp.get_type()}Resolver) ${gen_title_name(field.get_name())}() ${field.get_type()._type_go}Resolver{
    ${field.get_name()}Resolver := ${field.get_type()._type_go}Resolver{}
    for _, v := range r.r.${gen_title_name(field.get_name())} {
        t := ${field.get_base_type()}Resolver{&v}
        ${field.get_name()}Resolver = append(${field.get_name()}Resolver, t)
    }
    return ${field.get_name()}Resolver
        % endif
    % elif field.is_object():
func (r *${resp.get_type()}Resolver) ${gen_title_name(field.get_name())}() ${field.get_type()._type_go}Resolver{
    return ${field.get_type()._type_go}Resolver{&r.r.${gen_title_name(field.get_name())}}
    % else:
func (r *${resp.get_type()}Resolver) ${gen_title_name(field.get_name())}() ${field.get_type()._type_go} {
    return r.r.${gen_title_name(field.get_name())}
    % endif
}
% endfor
