package ${package_name}

import (
    "encoding/json"
    "errors"
)

const (
% for err_info in err_infos:
   ${err_info.code} int32 = ${err_info.number}
% endfor
)

var ErrMsg = map[int32]string {
% for err_info in err_infos:
    ${err_info.code}:"${err_info.msg}",
% endfor
}

type Error struct {
    Code int32    `json:"code"`
    Msg string    `json:"msg"`
	Detail string `json:"detail"`
}

func (ce *Error)Error()(error) {
    return errors.New(string(ce.Json()))
}

func (ce *Error)Json()([]byte) {
    s, _ := json.Marshal(ce)
    return s
}

func (ce *Error)String() string {
	return string(ce.Json())
}

func GenSuccess() *Error {
	return GenError(Success)
}

func FromJson(buf []byte)(*Error, error) {
    var ce Error
    err := json.Unmarshal(buf, &ce)
    if err != nil {
        return nil, err
    }
    return &ce, nil
}

// func GenJson(errCode int32) ([]byte) {
//     return (&Error{errCode, ErrMsg[errCode], ErrMsg[errCode]}).Json()
// }

func GenError(errCode int32) (*Error) {
	return &Error{errCode, ErrMsg[errCode], ""}
}

func GenErrorWithInfo(errCode int32, info string) (*Error) {
	return &Error{errCode, ErrMsg[errCode], info}
}
