CoordMode, Mouse

tab_x_pos := 800
tab_y_pos := 93

;关闭标签
Loop, 4
{
    Click %tab_x_pos%, %tab_y_pos%
    Sleep, 1000
}

;鼠标需要移动到中间位置
Click %tab_x_pos%, 384, 0

; Exit
;Exit

