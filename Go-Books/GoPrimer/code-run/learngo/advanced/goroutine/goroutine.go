package main

// 协程 Coroutine

import (
	"fmt"
	"runtime"
	"time"
)

func main() {
	var array [10]int
	for i := 0; i < 10; i++ {
		go func(i int) { // race condition
			for {
				array[i]++
				runtime.Gosched()
			}
		}(i)
	}

	time.Sleep(time.Millisecond)
	fmt.Println(array)
}
