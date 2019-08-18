package ${grpc_package_name}

import "golang.org/x/net/context"
import "${error_package}"
import protopb "${grpc_proto_dir}"

func (s *${grpc_service_type_name})${gen_upper_camel(api.name)}(ctx context.Context, req *protopb.${api.req.type.name}) (resp *protopb.${api.resp.type.name}, err error) {
	resp = &protopb.${api.resp.type.name}{}
	ec := errno.GenSuccess()
	defer func() {
		resp.Code = ec.Code
		resp.Msg = ec.Msg
	}()


	return
}
