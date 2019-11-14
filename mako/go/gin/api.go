<% import os %>
package ${package_name}

import "${package_go_gin_define}"
import "${package_service}/app/errno"
import "github.com/gin-gonic/gin"
// import "log"

func ${gen_lower_camel(api.name)}(ctx *gin.Context, urlParam *${os.path.basename(go_gin_define_dir)}.${api.url_param.type.name}, req *${os.path.basename(go_gin_define_dir)}.${api.req.type.name})(resp *${os.path.basename(go_gin_define_dir)}.${api.resp.type.name}) {
    // log.Info("req[%+v]", *req)
    // log.Info("urlParam[%+v]", *urlParam)
    resp = &${os.path.basename(go_gin_define_dir)}.${api.resp.type.name}{}
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
