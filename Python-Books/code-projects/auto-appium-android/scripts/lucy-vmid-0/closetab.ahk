CoordMode, Mouse

tab_x_pos := 218
tab_y_pos := 93

Click %tab_x_pos%, %tab_y_pos%

;鼠标需要移动到中间位置
end_x_post := %tab_x_pos% + 100
end_y_post := %tab_y_pos% + 300
Click %end_x_post%, %end_y_post%, 0

; Exit
;Exit

