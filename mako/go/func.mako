package service

import "${pro_path}/app/define"
import "context"

<%
    req = interface.get_req()
    resp = interface.get_resp()
    func_name = gen_title_name(interface.get_name())
%>

% if len(req.fields()) > 0:
func ${func_name}(ctx context.Context, ${req.get_name()} *define.${req.get_name()})(*define.${resp.get_name()}, error) {
% else:
func ${func_name}(ctx context.Context)(*define.${resp.get_name()}, error) {
% endif
    // code here
    ${resp.get_name()} := &define.${resp.get_name()}{}


    return ${resp.get_name()}, nil
}
