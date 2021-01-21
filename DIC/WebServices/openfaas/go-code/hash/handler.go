package function

import "fmt"
//import "time"
import "encoding/json"

// Handle a serverless request
func Handle(req []byte) string {
	msg := make(map[string]interface{})
	msg["msg"] = "Hello"
	mjson,_ :=json.Marshal(msg)
	mString :=string(mjson)
	return fmt.Sprintf(mString)
}
