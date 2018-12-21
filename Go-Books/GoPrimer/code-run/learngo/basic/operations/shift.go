package operations


// Left shift
// bitNumber 2**n
func UnsignedLeftShift(inputValue, bitNumber uint) (outValue uint){
	outValue = inputValue << bitNumber
	return outValue
}

// Right shift
func UnsignedRightShift(inputValue, bitNumber uint) (outValue uint){
	outValue = inputValue >> bitNumber
	return outValue
}