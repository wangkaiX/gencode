<% import os %>
package ${restful_api_package}

import "${package_restful_define_dir}"
import "${package_project_dir}/app/errno"
import "github.com/gin-gonic/gin"

func ${api.name}(ctx *gin.Context, ${api.url_param.name} *${os.path.basename(restful_define_dir)}.${api.url_param.type.name}, ${api.req.name} *${os.path.basename(restful_define_dir)}.${api.req.type.name})(${api.resp.name} *${os.path.basename(restful_define_dir)}.${api.resp.type.name}) {
    ${api.resp.name} = &${os.path.basename(restful_define_dir)}.${api.resp.type.name}{}
    var ec errno.Error
    defer func() {
        ${api.resp.name}.Code = ec.Code
        ${api.resp.name}.Msg = ec.Msg
    }()

    // code here


    return
}
