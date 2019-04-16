package define

// ${req.get_type()} 定义
type  ${req.get_type()} struct {
% for field in req.fields():
    // ${gen_title_name(field.get_name())}
    ${gen_title_name(field.get_name())} ${field.get_type()._type_go} // ${field.get_comment()}

% endfor
}

// ${resp.get_type()} 定义
type  ${resp.get_type()} struct {
% for field in resp.fields():
    // ${gen_title_name(field.get_name())}
    ${gen_title_name(field.get_name())} ${field.get_type()._type_go} // ${field.get_comment()}

% endfor
}

