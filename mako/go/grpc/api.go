package ${grpc_package}

import "golang.org/x/net/context"
import "${error_package}"
import protopb "${package_grpc_proto_dir}"
import "json"

// ${api.note}
func ${gen_upper_camel(api.name)}(ctx context.Context, req *protopb.${api.req.type.name}) (resp *protopb.${api.resp.type.name}, err error) {
	resp = &protopb.${api.resp.type.name}{}
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
