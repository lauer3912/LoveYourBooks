package variable_value_swap

/// Swap a and b,
/// **Restriction**: Don't use other variables
/// eg.
/// Input: a = 8, b = 12
/// Output: a = 12, b = 8
func SwapUseLikeCWay(a, b int) (int, int) {
	// 原理：数轴X上两点A和B，A和B数值内容交换
	if b >= a {
		a = b - a // A点与B点的距离
		b = b - a // A点的值给B
		a = b + a //
	} else {
		b = a - b
		a = a - b
		b = a + b
	}

	return a, b
}
