package service

import "${pro_path}/app/define"
import "context"

<%
    req = interface.get_req()
    resp = interface.get_resp()
    func_name = gen_title_name(interface.get_name())
%>

func ${func_name}(ctx context.Context, ${req.get_name()} *define.${req.get_name()})(*define.${resp.get_name()}, error) {
    // code here
    ${resp.get_name()} := &define.${resp.get_name()}{}


    return ${resp.get_name()}, nil
}
