// +build integration

package test

import (
    "fmt"
    "io/ioutil"
    "log"
    "net/http"
    "strings"
    "testing"
    "${package_service}/app/define"
)

func Test${gen_upper_camel(api.name)}(t *testing.T) {
    define.InitConfig("../../../configs/config.toml")
    client := http.Client{}
    input := `
        ${input_text}
               `

    request, err := http.NewRequest("POST", fmt.Sprintf("http://%v:%v${api.url}${url_param2text(api.url_param.fields)}", define.Cfg.HttpAddr.Ip, define.Cfg.HttpAddr.Port), strings.NewReader(input))
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
