package test

import (
    "fmt"
    "log"
    "testing"

    "context"

    "${pro_path}/app/define/graphqldefine"
    "github.com/machinebox/graphql"
)

<%
    interface_name = interface.get_name()
    resp = interface.get_resp()
%>

type ${interface_name}${resp.get_name()}_${name}Struct struct {
    ${gen_title_name(interface_name)} graphqldefine.${resp.get_name()}
}

##<%def name="gen_print(interface_name, fields)">
##% for field in fields:
##    fmt.Println(respData.${gen_title_name(interface_name)}.${gen_title_name(field.get_name())})
##% endfor
##</%def>

func Test${gen_title_name(interface_name)}${resp.get_name()}_${name}(t *testing.T) {
    client := graphql.NewClient("http://localhost:${port}/graphql")
    req := graphql.NewRequest(`${query_type} {
% if input_args == "":
    ${interface_name}() {
% else:
    ${interface_name}(${input_args}) {
% endif
        ${output_args}
        }
    }
    `)
    req.Header.Set("Cache-Control", "no-cache")
    req.Header.Set("sf_user_id", "622212323")
    var respData ${interface_name}${resp.get_name()}_${name}Struct
    ctx := context.Background()
    if err := client.Run(ctx, req, &respData); err != nil {
        log.Fatal(err)
    }   
    fmt.Println(respData)
## ${gen_print(interface_name, resp.fields())}
    fmt.Println("***********************************************************************************")
}
