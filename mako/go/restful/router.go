package restfulresolver

import "net/http"
import "github.com/gin-gonic/gin"
<%def name = "import_gin_file(apis)" >
% for api in apis:
    % for field in api.req.fields:
        % if field.type.name == 'GinFileInfort.FileHeader':
            <% return 'import "mime/multipart"' %>
        % endif
    % endfor
% endfor
    <% return "" %>
</%def>
${import_gin_file(apis)}

% for api in apis:
    % if len(api.req.fields) > 0:
import "${project_path}/app/define"
        <% break %>
    % endif
% endfor

import "${project_path}/app/service"

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
    %>
    router.${api.method}("/${api.url}", func(c *gin.Context) {
        var req define.${req.get_name()}
    % if len(url_param.fields) > 0:
        var param define.${url_param.type.name}
        if err := c.BindQuery(&param); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }
        % for field in url_param.fields:
        req.${gen_title_name(field.get_name())} = param.${gen_title_name(field.get_name())}
        % endfor
    % endif

    % if len(req.fields) > 0 or len(req.nodes) > 0:
        if err := c.Bind(&req); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }
    % endif

        resp := service.${api.name}(c, &req)
        c.JSON(http.StatusOK, resp) 
    })

% endfor

    return router.Run(addr)

}
