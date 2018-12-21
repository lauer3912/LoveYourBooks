package operations

import (
	"testing"
	bos "../../../basic/operations"
)

func TestUnsignedLeftShift(t *testing.T) {
	type CheckTable struct {
		Input, ShiftBitNumber, Except uint
	}

	testData := []CheckTable{
		{2, 1, 4}, // 10 -> 100
		{10, 1,  20}, // 1010 -> 10100
		{1240, 1, 2480},
		{2, 2, 8},
		{100, 4, 1600},
	}

	for _, ele := range testData {
		actual := bos.UnsignedLeftShift(ele.Input, ele.ShiftBitNumber)
		if actual != ele.Except {
			t.Errorf("UnsignedShiftLeft: input = %d, actual = %d, expect = %d",
				ele.Input,
				actual,
				ele.Except)
		}
	}

}

func TestUnsignedRightShift(t *testing.T) {
	type CheckTable struct {
		Input, ShiftBitNumber, Except uint
	}

	testData := []CheckTable{
		{4, 1, 2},    // 10 -> 100
		{20, 1,  10}, // 1010 -> 10100
		{2480, 1, 1240},
		{8, 2, 2},
		{1600, 4, 100},
	}

	for _, ele := range testData {
		actual := bos.UnsignedRightShift(ele.Input, ele.ShiftBitNumber)
		if actual != ele.Except {
			t.Errorf("UnsignedRightShift: input = %d, actual = %d, expect = %d",
				ele.Input,
				actual,
				ele.Except)
		}
	}

}