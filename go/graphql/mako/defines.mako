package define

// ${st.get_type()} 定义
type  ${st.get_type()} struct {
% for field in st.fields():
    // ${gen_title_name(field.get_name())}
    ${gen_title_name(field.get_name())} ${field.get_type()._type_go} // ${field.get_comment()}

% endfor
}
