package ${package_name}

import "golang.org/x/net/context"
import "${package_errno_dir}"
import pb "${package_proto_dir}"
import "encoding/json"

// ${api.note}
func ${gen_upper_camel(api.name)}(ctx context.Context, req *pb.${api.req.type.go}) (resp *pb.${api.resp.type.go}, err error) {
	resp = &pb.${api.resp.type.go}{}
    var ec *errno.Error
	defer func() {
        if ec == nil {
	        ec = errno.GenSuccess()
        }
		resp.Code = ec.Code
		resp.Msg = ec.Msg
	}()

    // code here


    // mock
    buf := []byte(`${json_output}`)
    err = json.Unmarshal(buf, resp)
	return
}
