package test

import (
    "fmt"
    "io/ioutil"
    "log"
    "net/http"
    "strings"
    "testing"
)

<%
    req = interface.get_req()
    resp = interface.get_resp()
    interface_name = interface.get_name()
    url = interface.get_url()
%>

func Test${gen_title_name(interface_name)}${resp.get_name()}_${name}(t *testing.T) {
    client := http.Client{}
    input := `
        ${input_args}
               `

    request, err := http.NewRequest("POST", "http://localhost:${port}/${url}?${url_param}", strings.NewReader(input))
    if err != nil {
        log.Fatal(err)
    }
    request.Header.Set("Content-Type", "application/json")
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
