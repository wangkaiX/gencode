package resolver

import "git.ucloudadmin.com/securehouse/ecosystem/dataflow/app/define"

% if req:
func (r *Resolver)${class_name}(ctx context.Context, args struct{
    ${req.get_type()} *${req.get_type()}
})(*${resp.get_type()}Resolver, error) {
    // code here


    return nil, nil
}
% else:
func (r *Resolver)${class_name}(ctx context.Context)(*${resp.get_type()}Resolver, error) {
    // code here


    return nil, nil
}
% endif
