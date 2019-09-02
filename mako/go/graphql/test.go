package test

import (
    "fmt"
    "log"
    "testing"
    "encoding/json"

    "context"

    "${package_graphql_define_dir}
    "github.com/machinebox/graphql"
)

<%
import os
%>

type ${api.resp.type.name}Test struct {
    ${gen_upper_camel(api.name)} ${os.path.basename(package_graphql_define_dir)}.${api.resp.name}
}

##<%def name="gen_print(interface_name, fields)">
##% for field in fields:
##    fmt.Println(respData.${gen_title_name(interface_name)}.${gen_title_name(field.get_name())})
##% endfor
##</%def>

func Test${gen_upper_camel(api.name)}(t *testing.T) {
    client := graphql.NewClient("http://localhost:${config_map['graphql_addr']['ip']}:${config_map['graphql_addr']['port']}/graphql")
    req := graphql.NewRequest(`${api.graphql_method} {
% if input_args == "":
    ${api.name}() {
% else:
    ${api.name}(${input_args}) {
% endif
        ${output_args}
        }
    }
    `)
    req.Header.Set("Cache-Control", "no-cache")
    req.Header.Set("sf_user_id", "622212323")
    var respData ${api.resp.type.name}Test
    ctx := context.Background()
    if err := client.Run(ctx, req, &respData); err != nil {
        log.Fatal(err)
    }   
    fmt.Println(respData)
    buf, _ := json.Marshal(&respData)
    fmt.Println(string(buf))
    fmt.Println("***********************************************************************************")
}
