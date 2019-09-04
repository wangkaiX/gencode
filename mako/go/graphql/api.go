package graphql_resolver

<%
    req = api.req
    resp = api.resp
    func_name = gen_upper_camel(api.name)
%>

import "${package_graphql_define_dir}"
import "context"
import "${package_graphql_api_dir}"
import "${error_package}"

% if len(req.fields) > 0:
func (r *${graphql_resolver_type_name})${func_name}(ctx context.Context, args struct{
    ${req.name} *${package_graphql_define_dir}.${req.name}
})(resp *${resp.name}Resolver, err error) {
% else:
func (r *Resolver)${func_name}(ctx context.Context)(resp *${resp.name}Resolver, err error) {
% endif
    resp = &${resp.name}Resolver{}
    var ec *errno.Error
    defer func() {
        if ec == nil {
            ec = errno.GenSuccess()
        }
        err = ec.Error()
    }()
    // code here


    return
}
