package function

import (
//	"fmt"
	"time"
	"encoding/json"
)

// Main function for the action
func Handle(req []byte) string {
	now:= time.Now()
	startTime := now.UnixNano() / 1e6

	name := "stranger"
	
	msg := make(map[string]interface{})
	msg["msg"] = "Hello, " + name + "!"
	msg["startTime"] =startTime

	mjson,_ :=json.Marshal(msg)
	mString :=string(mjson)
	
	return mString
}