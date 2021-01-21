package main

import (
    "crypto/md5"
 	"time"
	"fmt"
)

func Main(obj map[string]interface{}) map[string]interface{} {
    now:= time.Now()
    startTime := now.UnixNano() / 1e6

	str, ok := obj["param"].(string)
	
	if(!ok) {
		str = "user_name....."
	}

    md5Inst := md5.New()
    md5Inst.Write([]byte(str))
    result := md5Inst.Sum(nil)
    md5data := fmt.Sprintf("%x", result)

    msg := make(map[string]interface{})
    msg["token"] = string(md5data)
    msg["startTime"] = startTime

    return msg
}
