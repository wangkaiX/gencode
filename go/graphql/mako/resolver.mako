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
    % else:
func (r *${resp.get_type()}Resolver) ${gen_title_name(field.get_name())}() ${field.get_type()._type_go} {
    return r.r.${gen_title_name(field.get_name())}
    % endif
}

% endfor
