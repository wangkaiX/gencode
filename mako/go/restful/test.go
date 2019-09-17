// +build restfultest

package test

import (
    "fmt"
    "io/ioutil"
    "log"
    "net/http"
    "strings"
    "testing"
)

func Test${gen_upper_camel(api.name)}(t *testing.T) {
    client := http.Client{}
    input := `
        ${json_input}
               `

    request, err := http.NewRequest("POST", "http://${config_map['http_addr']['ip']}:${config_map['http_addr']['port']}${api.url}${api.url_param.url_param}", strings.NewReader(input))
    if err != nil {
        log.Fatal(err)
    }
    request.Header.Set("Content-Type", "application/json")
% for field in api.context.fields:
    request.Header.Set("${field.name}", "${field.value}")
% endfor
    respond, err := client.Do(request)
    if err != nil {
        log.Fatal("client do fatal:", err)
    }
    defer respond.Body.Close()
    body, err := ioutil.ReadAll(respond.Body)
    if err != nil {
        log.Fatal("read fatal:", err)
    }
    fmt.Println("respond:", respond)
    fmt.Println("body:", string(body))
}
