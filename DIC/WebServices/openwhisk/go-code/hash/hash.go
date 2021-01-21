package main

import (
    "crypto/sha1"
    "fmt"
    "time"
)

func Main(obj map[string]interface{}) map[string]interface{} {
    now:= time.Now()
    startTime := now.UnixNano() / 1e6

    str, ok := obj["param"].(string)

    if(!ok){
        str = "hashtest"
    }

    h := sha1.New()
    h.Write([]byte(str))
    bs := h.Sum(nil)
    sha1data := fmt.Sprintf("%x", bs)

    msg := make(map[string]interface{})
    msg["token"] = string(sha1data)
    msg["startTime"] = startTime

    return msg
}
