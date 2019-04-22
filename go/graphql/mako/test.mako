package test

import (
    "fmt"
    "log"
    "testing"

    "context"

    "git.ucloudadmin.com/securehouse/dataflow/dataviewer/app/define"
    "github.com/machinebox/graphql"
)

type ${resp.get_name()}Struct struct {
    ${resp.get_name()} define.${resp.get_type()}
}

##<%def name='get_field(fields)'>
##    % for field in fields:
##        % if field.is_object():
##            // 对象
##            ${field.get_name()}{
##                <% return get_field(resps[field.get_type()].fields()) %>
##            }
##        % elif field.is_list():
##            <% pass %>
##        % else:
##            // 不是对象
##            ${gen_title_name(field.get_name())}
##        % endif
##    % endfor
##</%def>

func Test${resp.get_name()}(t *testing.T) {
    client := graphql.NewClient("http://localhost:40011/graphql")
    req := graphql.NewRequest(`${query_type} {
        ${interface_name} {
            ${get_field(resp.fields())}
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
    fmt.Println(respData.${resp.get_name()}.${gen_title_name(field.get_name())})
% endfor
}
