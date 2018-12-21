package simple

import (
	"fmt"
	"time"
)

func handlerWorker(id int, c chan int) {
	for value := range c{
		fmt.Printf("Worker %d received %d \n", id, value)
	}
}

func createWorker(id int) chan<- int {
	c := make(chan int)
	go handlerWorker(id, c)
	return c
}

func chanDemo() {
	var channels [10] chan<- int
	for i:=0; i<10; i++ {
		channels[i] = createWorker(i)
	}

	for i:=0; i<10; i++ {
		channels[i] <- 'a' + i
	}

	for i:=0; i<10; i++ {
		channels[i] <- 'A' + i
	}

	time.Sleep(time.Millisecond)
}

func channelCloseDemo() {
	c := make(chan int)

	c <- 'a'
	c <- 'b'
	c <- 'c'
	c <- 'd'
	close(c)

	time.Sleep(time.Millisecond)
}

func bufferedChannel() {
	c := make(chan int, 3)
	go handlerWorker(0, c)
	c <- 1
	c <- 2
	c <- 3
	c <- 4

	time.Sleep(time.Millisecond)
}




const (
	UseChannelCloseDemo  = 1
	UseChanDemo = 2
	UseBufferedChannel = 3

)


func main() {
	useWay := UseBufferedChannel

	switch useWay {
	case UseChanDemo:
		chanDemo()
	case UseChannelCloseDemo:
		channelCloseDemo()
	case UseBufferedChannel:
		bufferedChannel()
	}
}
