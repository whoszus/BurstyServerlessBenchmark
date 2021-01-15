package main

import (
	"fmt"
	"time"
)

// Main function for the action
func Main(obj map[string]interface{}) map[string]interface{} {
	now:= time.Now()
	startTime := now.UnixNano() / 1e6
	name, ok := obj["name"].(string)
	if !ok {
		name = "stranger"
	}
	fmt.Printf("name=%s\n", name)
	msg := make(map[string]interface{})
	msg["msg"] = "Hello, " + name + "!"
	msg["startTime"] =startTime
	return msg
}