package main

import "time"

func partition(a []int, lo, hi int) int {
	p := a[hi]
	for j := lo; j < hi; j++ {
		if a[j] < p {
			a[j], a[lo] = a[lo], a[j]
			lo++
		}
	}

	a[lo], a[hi] = a[hi], a[lo]
	return lo
}

func quickSort(a []int, lo, hi int) {
	if lo > hi {
		return
	}

	p := partition(a, lo, hi)
	quickSort(a, lo, p-1)
	quickSort(a, p+1, hi)
}

func Main(obj map[string]interface{}) map[string]interface{} {
	now:= time.Now()
    startTime := now.UnixNano() / 1e6
 
    list := []int{3, 6, 8, 10, 1, 2, 1, 4, 5, 6, 7, 8, 2232, 2, 4, 5, 7, 9, 20, 0, 88, 7, 34}
	
	quickSort(list, 0, len(list)-1)

	msg := make(map[string]interface{})
    msg["token"] = "sort finished"
	msg["startTime"] = startTime
	
	return msg
}