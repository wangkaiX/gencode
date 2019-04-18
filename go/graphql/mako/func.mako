package resolver

import "git.ucloudadmin.com/securehouse/dataflow/dataviewer/app/define"
import "context"

% if req:
func (r *Resolver)${class_name}(ctx context.Context, args struct{
    ${req.get_type()} *define.${req.get_type()}
})(*${resp.get_type()}Resolver, error) {
% else:
func (r *Resolver)${class_name}(ctx context.Context)(*${resp.get_type()}Resolver, error) {
% endif
    // code here


    return &${resp.get_type()}Resolver{&define.${resp.get_type()}{}}, nil
}
