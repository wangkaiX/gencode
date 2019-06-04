package restfulresolver

import "net/http"
import "context"

import "github.com/gin-gonic/gin"

% for interface in all_interface:
    % if len(interface.get_req().fields()) > 0:
import "${pro_path}/app/define"
        <% break %>
    % endif
% endfor

import "${pro_path}/app/service"

func Run(addr string)(err error) {
    gin.SetMode(gin.ReleaseMode)
    var router = gin.Default()
% for interface in all_interface:
    <%
        req = interface.get_req()
        resp = interface.get_resp()
        func_name = gen_title_name(interface.get_name())
        interface_name = interface.get_name()
        url = interface.get_url()
        urlparam = interface.get_url_param()
    %>
    router.POST("/${url}", func(c *gin.Context) {
        var req define.${req.get_name()}
    % if len(urlparam.fields()) > 0:
        var param define.${urlparam.get_name()}
        if err := c.BindQuery(&param); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }
        % for field in urlparam.fields():
        req.${gen_title_name(field.get_name())} = param.${gen_title_name(field.get_name())}
        % endfor
    % endif

    % if len(req.fields()) > 0:
        if err := c.BindJSON(&req); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }
    % endif

        resp, _ := service.${func_name}(context.Background(), &req)
        c.JSON(http.StatusOK, resp) 
    })

% endfor

    return router.Run(addr)

}
