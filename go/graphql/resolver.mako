package resolver

import "git.ucloudadmin.com/securehouse/ecosystem/projectmanager/defines"

type ${gen_title(resp.get_name())}Resolver struct {
    r *defines.RegionInfo
}

% for field in resp.get_fields():
func (r *${gen_title(resp.get_name())}) ${gen_title(field.get_name())}() ${field.get_type()} {
    return r.r.${gen_title(field.get_name())}
}

% endfor
