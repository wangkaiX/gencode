package resolver

import "${pro_path}/app/define"
import "context"

<%
    req = interface.get_req()
    resp = interface.get_resp()
    func_name = gen_title_name(interface.get_name())
%>

% if len(req.fields()) > 0:
func (r *Resolver)${func_name}(ctx context.Context, args struct{
    ${req.get_name()} *define.${req.get_name()}
})(*${resp.get_name()}Resolver, error) {
% else:
func (r *Resolver)${func_name}(ctx context.Context)(*${resp.get_name()}Resolver, error) {
% endif
    // code here
    ${resp.get_name()} := &define.${resp.get_name()}{}


    return &${resp.get_name()}Resolver{${resp.get_name()}}, nil
}
