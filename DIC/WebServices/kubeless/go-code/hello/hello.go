package kubeless

import (
	"time"
	"github.com/kubeless/kubeless/pkg/functions"
	"encoding/json"
)

// Main function for the action
func Handler(event functions.Event, context functions.Context) (string, error) {
	now:= time.Now()
	startTime := now.UnixNano() / 1e6

	name := "stranger"

	msg := make(map[string]interface{})
	msg["msg"] = "Hello, " + name + "!"
	msg["startTime"] =startTime

	//change to string
	mjson,_ :=json.Marshal(msg)
	mString :=string(mjson)

	return mString, nil
}