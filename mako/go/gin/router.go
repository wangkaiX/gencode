package ${package_name}
// 不要修改此文件

import "net/http"
import "github.com/gin-gonic/gin"

% for api in apis:
    % if len(api.req.fields) > 0:
import "${package_define}"
        <% break %>
    % endif
% endfor

func Run(addr string)(err error) {
    gin.SetMode(gin.ReleaseMode)
    var router = gin.Default()
% for api in apis:
    <%
        req = api.req
        resp = api.resp
        func_name = api.name
        interface_name = api.name
        url_param = api.url_param
        import os
        define = os.path.basename(package_define)
    %>
    router.${api.method}("${api.url}", func(c *gin.Context) {
		var req ${define}.${req.type.name}
		var param ${define}.${url_param.type.name}
    % if len(url_param.fields) > 0:
        if err := c.BindQuery(&param); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }
    % endif

    % if len(req.fields) > 0 or len(req.nodes) > 0:
        if err := c.Bind(&req); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }
    % endif

        resp := ${gen_lower_camel(api.name)}(c, &param, &req)
        c.JSON(http.StatusOK, resp)
    })

% endfor

    return router.Run(addr)

}
