package define

import "mime/multipart"

// GinFileInfo 定义
type GinFileInfo struct {
	File multipart.File `form:"-"`

	Header *multipart.FileHeader `form:"-"`

	Error error `form:"-"`
}
