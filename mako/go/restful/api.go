package service

import "${project_path}/app/define"
import "${project_path}/app/errno"
import "github.com/gin-gonic/gin"

func ${api.name}(ctx *gin.Context, ${api.req.name} *define.${api.req.type.name})(${resp.name} *define.${resp.type.name}) {
    // code here
    ${resp.name} = &define.${resp.type.name}{}
    var ec errno.Error
    defer func() {
        ${resp.name}.Code = ec.Code
        ${resp.name}.Msg = ec.Msg
    }()


    return
}
