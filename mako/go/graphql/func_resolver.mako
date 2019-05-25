package resolver

<%
    req = interface.get_req()
    resp = interface.get_resp()
    func_name = gen_title_name(interface.get_name())
%>

import "${pro_path}/app/define/graphql_define"
import "context"
import "${pro_path}/app/service"

% if len(req.fields()) > 0:
func (r *Resolver)${func_name}(ctx context.Context, args struct{
    ${req.get_name()} *graphql_define.${req.get_name()}
})(*${resp.get_name()}Resolver, error) {
% else:
func (r *Resolver)${func_name}(ctx context.Context)(*${resp.get_name()}Resolver, error) {
% endif
    // code here
% if len(req.fields()) > 0:
    resp, err := service.${func_name}(ctx, graphql_define.ToDefine${req.get_name()}(args.${req.get_name()}))
% else:
    resp, err := service.${func_name}(ctx)
% endif
    return &${resp.get_name()}Resolver{graphql_define.ToGraphqlDefine${resp.get_name()}(resp)}, err
}
