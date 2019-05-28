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
    %>
    router.POST("/${interface_name}", func(c *gin.Context) {
    % if len(req.fields()) > 0:
        var req define.${req.get_name()}
        if err := c.ShouldBindJSON(&req); err != nil {
            if err = c.ShouldBind(&req); err != nil {
                c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
                return
            }
        }

        resp, _ := service.${func_name}(context.Background(), &req)
    % else:
        resp, _ := service.${func_name}(context.Background())
    % endif

        // if err != nil {
        //     c.JSON(http.StatusOK, err)
        //     return
        // }
  
        c.JSON(http.StatusOK, resp) 
    })

% endfor

    return router.Run(addr)

}
