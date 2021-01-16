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

    Sha1Inst := sha1.New()
    Sha1Inst.Write([]byte(str))
    result = Sha1Inst.Sum([]byte(""))
    sha1data := fmt.Sprintf("%x", result)

    msg := make(map[string]interface{})
    msg["token"] = string(sha1data)
    msg["startTime"] = startTime

    return msg
}
