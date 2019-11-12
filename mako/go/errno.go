package ${package_name}

// 不要修改此文件

import (
    "encoding/json"
    "errors"
)

const (
% for errno in errnos:
   ${errno.code} int32 = ${errno.no}
% endfor
)

var ErrMsg = map[int32]string {
% for errno in errnos:
    ${errno.code}:"${errno.msg}",
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

func GenErrorWithDetail(errCode int32, info string) (*Error) {
    return &Error{errCode, fmt.Sprintf("%s:[%s]", ErrMsg[errCode], info), info}
}
