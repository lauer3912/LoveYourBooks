package variable_value_swap

// Swap a and b,
// **Restriction**: Don't use other variables
// eg.
// Input: a = 8, b = 12
// Output: a = 12, b = 8
func SwapUseGoFuncWay(a, b int) (int, int) {
	// Go language is **"value copy transfer(值传递)"**
	// So that, the variables a and b ,is not input source a and b

	return b, a
}

// Swap a and b, use a pointer and b pointer
// like c language value swap
func SwapUseGoPointerWay(a, b *int) (int, int) {
	// NOTE: Go language doesn't supports the pointer operation, eg. plus,
	// So, must use the real value to do it.
	// 原理：数轴X上两点A和B，A和B数值内容交换
	if *b >= *a {
		*a = *b - *a // A点与B点的距离
		*b = *b - *a // A点的值给B
		*a = *b + *a //
	} else {
		*b = *a - *b
		*a = *a - *b
		*b = *a + *b
	}

	return *a, *b

}

// Swap a and b, use the displacement operator
func SwapUseGoDisplacementWay(a, b int) (int, int) {
	// NOTE: Any number is consecutive xor from any given other number value, and the original number value is unchanged.
	a = a ^ b
	b = a ^ b
	a = a ^ b
	return a, b
}
