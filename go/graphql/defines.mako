type  ${req.get_name()} struct {
% for field in req.get_fields():
    ${field.get_name()} ${field.get_type()} // ${field.get_comment()}

% endfor
}

type  ${resp.get_name()} struct {
% for field in resp.get_fields():
    ${field.get_name()} ${field.get_type()} // ${field.get_comment()}

% endfor
}

