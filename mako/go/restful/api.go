<% import os %>
package ${restful_api_package}

import "${package_restful_define_dir}"
import "${package_project_dir}/app/errno"
import "github.com/gin-gonic/gin"

func ${gen_lower_camel(api.name)}(ctx *gin.Context, urlParam *${os.path.basename(restful_define_dir)}.${api.url_param.type.name}, req *${os.path.basename(restful_define_dir)}.${api.req.type.name})(resp *${os.path.basename(restful_define_dir)}.${api.resp.type.name}) {
    resp = &${os.path.basename(restful_define_dir)}.${api.resp.type.name}{}
    var ec *errno.Error
    defer func() {
        if ec == nil {
            ec = errno.GenSuccess()
        }
        resp.Code = ec.Code
        resp.Msg = ec.Msg
    }()

    // code here


    return
}
