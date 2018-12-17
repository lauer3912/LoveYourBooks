package reverse

import (
	rs "../../../basic/reverse"
	"fmt"
)

import "testing"

type ResultUnit struct {
	ele    *rs.SimpleList
	expect string
}

func getSimpleTestData() ResultUnit {

	//origin
	obj4 := rs.SimpleList{
		4, nil,
	}
	obj3 := rs.SimpleList{
		3, &obj4,
	}
	obj2 := rs.SimpleList{
		2, &obj3,
	}
	obj1 := rs.SimpleList{
		1, &obj2,
	}

	dataTable := ResultUnit{
		&obj1,
		"4321",
	}

	return dataTable
}

func TestSimpleListUseCustomReverseFunction(t *testing.T) {
	item := getSimpleTestData()
	orgList := item.ele

	// Print the actual data
	fmt.Println("orgList value = ", orgList.PrintDataString())
	reverse_list := orgList.CustomReverse()
	actual := reverse_list.PrintDataString()
	fmt.Println("reverse_list value = ", actual)

	// Test
	if actual != item.expect {
		t.Errorf("%v actualData = %s, expectData = %s",
			"CustomReverse",
			actual,
			item.expect,
		)
	}
}

func TestSimpleListUseImplementReverseMethod(t *testing.T) {

}
