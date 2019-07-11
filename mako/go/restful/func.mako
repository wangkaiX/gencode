package service

import "${pro_path}/app/define"
import "${pro_path}/app/errno"
import "github.com/gin-gonic/gin"

<%
    req = interface.get_req()
    resp = interface.get_resp()
    func_name = gen_title_name(interface.get_name())
%>

func ${func_name}(ctx *gin.Context, ${req.get_name()} *define.${req.get_name()})(${resp.get_name()} *define.${resp.get_name()}) {
    // code here
    ${resp.get_name()} = &define.${resp.get_name()}{}
    var ec errno.Error
    defer func() {
        ${resp.get_name()}.Code = ec.Code
        ${resp.get_name()}.Msg = ec.Msg
    }()


    return
}
