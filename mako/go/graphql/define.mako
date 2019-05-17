package define

% for field in st.fields():
    % if 'time.Time' == field.get_type()._go:
import "time"
        <% break %>
    % endif
% endfor

// ${st.get_name()} ${st.get_comment()}
type  ${st.get_name()} struct {
% for field in st.fields():
##// ${gen_title_name(field.get_name())}
% if st.is_req() and field.is_necessary():
    % if field.is_list():
    ${gen_title_name(field.get_name())} []*${field.get_type()._go} // ${field.get_comment()}
    % else:
    ${gen_title_name(field.get_name())} ${field.get_type()._go} // ${field.get_comment()}
    % endif
% elif st.is_req() and not field.is_necessary():
    % if field.is_list():
    ${gen_title_name(field.get_name())} *[]*${field.get_type()._go} // ${field.get_comment()}
    % else:
    ${gen_title_name(field.get_name())} *${field.get_type()._go} // ${field.get_comment()}
    % endif
% elif st.is_resp():
    % if field.is_list():
    ${gen_title_name(field.get_name())} []${field.get_type()._go} `db:"${to_underline(field.get_name())}"`// ${field.get_comment()}
    % else:
    ${gen_title_name(field.get_name())} ${field.get_type()._go} `db:"${to_underline(field.get_name())}"`// ${field.get_comment()}
    % endif
% else:
    ${gen_title_name(field.get_name())} *${field.get_type()._go} // ${field.get_comment()}
% endif

% endfor
}
