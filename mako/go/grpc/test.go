package testgrpc

import (
    pb "${grpc_proto_dir}"
    "fmt"
    "log"
    "testing"
	"encoding/json"

    "golang.org/x/net/context"

    "google.golang.org/grpc"
)

func Test${gen_upper_camel(api.name)}(t *testing.T) {
    conn, err := grpc.Dial("${grpc_ip}:${grpc_port}", grpc.WithInsecure())
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

    ctx := context.Background()
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
