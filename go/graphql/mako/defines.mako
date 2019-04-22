package define

% for field in st.fields():
    % if 'time.Time' == field.get_type()._go:
import "time"
        <% break %>
    % endif
% endfor

// ${st.get_type()} 定义
type  ${st.get_type()} struct {
% for field in st.fields():
    // ${gen_title_name(field.get_name())}
% if field.is_necessary():
    ${gen_title_name(field.get_name())} ${field.get_type()._go} // ${field.get_comment()}
% elif is_response:
    ${gen_title_name(field.get_name())} ${field.get_type()._go} `db:"${to_underline(field.get_name())}"`// ${field.get_comment()}
% else:
    ${gen_title_name(field.get_name())} *${field.get_type()._go} // ${field.get_comment()}
% endif

% endfor
}
