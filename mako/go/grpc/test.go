// +build integration

package testgrpc
// 不要修改此文件

import (
    pb "${package_grpc_proto_dir}"
    "fmt"
    "log"
    "testing"
	"encoding/json"

    "golang.org/x/net/context"

    "google.golang.org/grpc"
    "google.golang.org/grpc/metadata"
)

func Test${gen_upper_camel(api.name)}(t *testing.T) {
    conn, err := grpc.Dial("${config_map['grpc_addr']['ip']}:${config_map['grpc_addr']['port']}", grpc.WithInsecure())
    if err != nil {
        log.Fatal(err)
    }
    client := pb.New${gen_upper_camel(grpc_service_name)}Client(conn)
    in := &pb.${gen_upper_camel(api.req.name)}{}
	buf := []byte(`${json_input}`)
	err = json.Unmarshal(buf, in)
    if err != nil {
        log.Fatal(err)
    }
	buf, err = json.Marshal(in)
	if err != nil {
        log.Fatal(err)
    }
	fmt.Printf("test:[%v]\n", string(buf))

    <%
        template = '"%s","%s",' 
        kv_list = ""
        for field in api.context.fields:
            kv_list = kv_list + template % (field.name, field.value)
    %>
    md := metadata.Pairs(${kv_list[:-1]})
    ctx := metadata.NewOutgoingContext(context.Background(), md)
    out, err := client.${gen_upper_camel(api.name)}(ctx, in)
	if err != nil {
        log.Fatal(err)
    }

	buf, err = json.Marshal(out)
	if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("[%v]\n", string(buf))
}
