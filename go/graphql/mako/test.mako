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

##<%def name='get_field(field)'>
##    % if field.is_object():
##        <% return field + '{ + get_field(field) + '}' %>
##    % else:
##        <% return field %>
##    % endif
##</%def>

func Test${resp.get_name()}(t *testing.T) {
    client := graphql.NewClient("http://localhost:40011/graphql")
    req := graphql.NewRequest(`${query_type} {
        ${interface_name} {
        % for field in resp.fields():
            ${field.get_name()}
        % endfor
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
