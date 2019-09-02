package ${grpc_package}

import "golang.org/x/net/context"
import protopb "${package_grpc_proto_dir}"

% for api in apis:

// ${api.note}
func (s *${grpc_service_type})${gen_upper_camel(api.name)}(ctx context.Context, req *protopb.${api.req.type.name}) (resp *protopb.${api.resp.type.name}, err error) {
	resp = &protopb.${api.resp.type.name}{}
	% for field in api.req.fields:
		% if field.required and field.type.name == 'string':
	if req.${gen_upper_camel(field.name)} == "" {
		resp.Code = -1
		resp.Msg = "缺少参数${field.name}"
		return
	}
		% endif 
	% endfor

	return ${gen_upper_camel(api.name)}(ctx, req)
}

% endfor
