package ${package_name}
// 不要修改此文件

import "golang.org/x/net/context"
import pb "${package_proto_dir}"

% for api in apis:

// ${api.note}
func (s *${grpc_service_type})${gen_upper_camel(api.name)}(ctx context.Context, req *pb.${api.req.type.go}) (resp *pb.${api.resp.type.go}, err error) {
	resp = &pb.${api.resp.type.go}{}
	% for field in api.req.fields:
		% if field.required and field.type.go == 'string':
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
