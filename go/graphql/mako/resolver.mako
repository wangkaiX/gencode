package resolver

import "git.ucloudadmin.com/securehouse/ecosystem/projectmanager/define"

type ${resp.get_type()}Resolver struct {
    r *defines.${resp.get_type()}
}

% for field in resp.fields():
func (r *${resp.get_name()}) ${gen_title_name(field.get_name())}() ${field.get_type()._type_go} {
    return r.r.${gen_title_name(field.get_name())}
}

% endfor

func (r *Resolver)${class_name}(ctx context.Context, args struct{
    ${req.get_type()} ${req.get_type()}
})(*${resp.get_type()}Resolver, error) {
    // code here


    return nil, nil
}
