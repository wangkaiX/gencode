package resolver

import "git.ucloudadmin.com/securehouse/dataflow/dataviewer/app/define"

type ${resp.get_type()}Resolver struct {
    r *define.${resp.get_type()}
}

% for field in resp.fields():
func (r *${resp.get_type()}Resolver) ${gen_title_name(field.get_name())}() ${field.get_type()._type_go} {
    % if field.is_necessary():
    return r.r.${gen_title_name(field.get_name())}
    % else:
    return r.r.${gen_title_name(field.get_name())}
    % endif
}

% endfor
