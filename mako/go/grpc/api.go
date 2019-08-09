package ${package_name}

import "golang.org/x/net/context"
import "${error_package}"
import protopb "${project_path}/proto"

func (s *${service_name})${gen_upper_camel(api.name)}(ctx context.Context, req *protopb.${api.req.type.name}) (resp *protopb.${api.resp.type.name}, err error) {
	resp = &protopb.${api.resp.type.name}{}
	ec := errno.GenSuccess()
	defer func() {
		resp.Code = ec.Code
		resp.Msg = ec.Msg
	}()


	return
}
