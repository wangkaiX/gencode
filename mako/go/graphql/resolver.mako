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
    <%
        ret_type = field.get_type()._go
        if field.is_enum() or field.is_list_enum():
            ret_type = 'string'
    %>
    % if field.is_list():
func (r *${resp.get_name()}Resolver) ${gen_title_name(field.get_name())}() []${ret_type} {
    % else:
func (r *${resp.get_name()}Resolver) ${gen_title_name(field.get_name())}() ${ret_type} {
    % endif
    return r.r.${gen_title_name(field.get_name())}
}

% endfor

% for node in resp.get_nodes():
    % if type(node) == list:
        <% node_t = node[0] %>
    % else:
        <% node_t = node %>
    % endif
    <%
        type_t = gen_title_name(node_t.get_name())
        type_resolver = type_t + 'Resolver'
        var = node_t.get_field_name()
        var_resolver = var + 'Resolver'
    %>
    % if type(node) == list:
func (r *${resp.get_name()}Resolver) ${gen_title_name(var)}() *[]*${type_resolver} {
   ${var_resolver} := []*${type_resolver}{}
   for _, v := range r.r.${gen_title_name(var)} {
       t := ${type_resolver}{&v}
       ${var_resolver} = append(${var_resolver}, &t) 
   }   
   return &${var_resolver}
}
    % else:
func (r *${resp.get_name()}Resolver) ${gen_title_name(var)}() *${type_resolver} {
    return &${type_resolver}{&r.r.${gen_title_name(var)}}
}
    % endif
% endfor
