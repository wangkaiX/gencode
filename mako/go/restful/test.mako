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
%>

func Test${gen_title_name(interface_name)}${resp.get_name()}_${name}(t *testing.T) {
    client := http.Client{}
    input := `
        ${input_args}
               `

    request, err := http.NewRequest("POST", "http://localhost:${port}/${interface_name}", strings.NewReader(input))
    if err != nil {
        log.Fatal(err)
    }
    request.Header.Set("Content-Type", "application/x-www-form-urlencoded")
    respond, err := client.Do(request)
    if err != nil {
        log.Fatal(err)
    }
    defer respond.Body.Close()
    body, err := ioutil.ReadAll(respond.Body)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(string(body))
}
