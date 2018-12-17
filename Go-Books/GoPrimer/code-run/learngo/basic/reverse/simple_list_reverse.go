package reverse

import "fmt"

// NOTE: Custom define a single list
type SimpleList struct {
	Data int
	Next *SimpleList
}

func (list *SimpleList) PrintDataString() string {
	if &list == nil {
		return ""
	}

	cur := list
	dataStr := ""
	for cur.Next != nil {
		dataStr = fmt.Sprintf("%v%v", dataStr, cur.Data)
		cur = cur.Next
	}

	if cur.Next == nil {
		dataStr = fmt.Sprintf("%v%v", dataStr, cur.Data)
	}

	return dataStr
}

// Defined custom reverse function for the SimpleList struct
func (head *SimpleList) CustomReverse() *SimpleList {
	if head == nil {
		return nil
	}

	pre := head
	cur := head.Next

	for cur != nil {
		nxt := cur.Next

		cur.Next = pre
		pre = cur
		cur = nxt
	}
	head.Next = nil

	return pre
}

// Implement the Reverse Interface methods
