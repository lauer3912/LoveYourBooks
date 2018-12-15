package variable_value_swap

/// Swap a and b,
/// **Restriction**: Don't use other variables
/// eg.
/// Input: a = 8, b = 12
/// Output: a = 12, b = 8
func SwapUseGoFuncWay(a, b int) (int, int) {
	// Go language is "value copy transfer"
	// So the variables a and b ,is not input source a and b

	return b, a
}
