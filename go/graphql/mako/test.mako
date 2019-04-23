package test

import (
    "fmt"
    "log"
    "testing"

    "context"

    "${package}/app/define"
    "github.com/machinebox/graphql"
)

type ${resp.get_name()}Struct struct {
    ${gen_title_name(interface_name)} define.${resp.get_type()}
}

func Test${resp.get_name()}(t *testing.T) {
    client := graphql.NewClient("http://localhost:40011/graphql")
    req := graphql.NewRequest(`${query_type} {
% if input_args == "":
    ${interface_name}() {
% else:
    ${interface_name}(${input_args}) {
% endif
${get_field(resp.fields(), resps)}
        }
    }
    `)
    req.Header.Set("Cache-Control", "no-cache")
    var respData ${resp.get_name()}Struct
    ctx := context.Background()
    if err := client.Run(ctx, req, &respData); err != nil {
        log.Fatal(err)
    }   
% for field in resp.fields():
    fmt.Println(respData.${gen_title_name(interface_name)}.${gen_title_name(field.get_name())})
% endfor
    fmt.Println("***********************************************************************************")
}
