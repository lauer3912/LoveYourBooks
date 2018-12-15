package basic

import (
	"math/rand"
	"reflect"
	"runtime"
	"testing"
)

import vvs "../../basic/variable_value_swap"

// NOTE:
// ```bash
// Run the go test
// $ go test .
//
// See the code coverage result
// $ go tool cover
// ```

type TestDataTable struct{ A1, B1, A2, B2 int }

func getStandData() []TestDataTable {
	return []TestDataTable{
		{3, 4, 4, 3},
		{6, 7, 7, 6},
		{16, 17, 17, 16},
		{26, 27, 27, 26},
		{36, 37, 37, 36},
		{99, 50, 50, 99},
		{77, 37, 37, 77},
	}
}

func getBigData() []TestDataTable {
	table := []TestDataTable{}

	for i := 0; i <= 10000000; i++ {
		leftValue, rightValue := rand.Int(), rand.Int()
		table = append(table, TestDataTable{
			A1: leftValue + i,
			B1: rightValue + i,
			A2: rightValue + i,
			B2: leftValue + i,
		})
	}
	return table
}

var funcArray = []func(int, int) (int, int){
	vvs.SwapUseGoFuncWay,
	vvs.SwapUseLikeCWay,
}

// TestXxx
func TestSwap(t *testing.T) {
	for _, curFun := range funcArray {
		for _, ele := range getStandData() {
			if actualA, actualB := curFun(ele.A1, ele.B1); actualA != ele.A2 || actualB != ele.B2 {
				funcName := runtime.FuncForPC(reflect.ValueOf(curFun).Pointer()).Name()
				t.Errorf("%v (%d, %d); "+
					"got (%d, %d); expected (%d, %d)",
					funcName,
					ele.A1, ele.B1,
					actualA, actualB,
					ele.A2, ele.B2)
			}
		}
	}
}

// BenchmarkXxx
// NOTE: Check ->  Is Graphviz installed?
//		 Install -> See http://graphviz.org/
//                 (1) onMac:
//							 $ brew install Graphviz
// ```bash
// $ go test -bench . -cpuprofile cpu.out
// $ go tool pprof cpu.out
// $ (pprof) web
// ```
func BenchmarkSwap(b *testing.B) {
	// Prepare the test data
	ele := getBigData()[3:4][0]

	// Don't contains the prepare data time
	b.ResetTimer()

	// Core operation
	for _, curFun := range funcArray {
		if actualA, actualB := curFun(ele.A1, ele.B1); actualA != ele.A2 || actualB != ele.B2 {
			funcName := runtime.FuncForPC(reflect.ValueOf(curFun).Pointer()).Name()
			b.Errorf("%v (%d, %d); "+
				"got (%d, %d); expected (%d, %d)",
				funcName,
				ele.A1, ele.B1,
				actualA, actualB,
				ele.A2, ele.B2)
		}
	}
}
