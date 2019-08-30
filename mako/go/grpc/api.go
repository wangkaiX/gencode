package ${grpc_package_name}

import "golang.org/x/net/context"
import "${error_package}"
import protopb "${package_grpc_proto_dir}"

// ${api.note}
func ${gen_upper_camel(api.name)}(ctx context.Context, req *protopb.${api.req.type.name}) (resp *protopb.${api.resp.type.name}, err error) {
	resp = &protopb.${api.resp.type.name}{}
	ec := errno.GenSuccess()
	defer func() {
		resp.Code = ec.Code
		resp.Msg = ec.Msg
	}()


	return
}
