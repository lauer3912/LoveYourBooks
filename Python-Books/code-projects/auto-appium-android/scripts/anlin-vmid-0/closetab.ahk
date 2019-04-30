CoordMode, Mouse

tab_x_pos := 218
tab_y_pos := 93
vm_offest := 0

;关闭标签
fnc_close_tab(x_pos, y_pos)
{
    Click %x_pos%, %y_pos%
    Sleep, 1000
}
fnc_close_tab(tab_x_pos, tab_y_pos)
fnc_close_tab(tab_x_pos, tab_y_pos)
fnc_close_tab(tab_x_pos, tab_y_pos)
fnc_close_tab(tab_x_pos, tab_y_pos)
fnc_close_tab(tab_x_pos, tab_y_pos)


ClearCache(offest)
{
    ;Clear All Cache
    cur_x_pos := 514 + offest
    Click %cur_x_pos%, 102
    Sleep, 1200
    
    ;Setting
    cur_x_pos := 350 + offest
    Click %cur_x_pos%, 186
    Sleep, 1200
    
    ;Privacy
    cur_x_pos := 58 + offest
    Click %cur_x_pos%, 390
    Sleep, 1200
    
    ;Clear browsing data
    cur_x_pos := 108 + offest
    Click %cur_x_pos%, 740
    Sleep, 1200
    
    ;ADVANCED
    cur_x_pos := 400 + offest
    Click %cur_x_pos%, 148
    Sleep, 1200
    
    ;All time
    cur_x_pos := 468 + offest
    Click %cur_x_pos%, 200
    Sleep, 1200
    
    ;All time2
    cur_x_pos := 438 + offest
    Click %cur_x_pos%, 366
    Sleep, 1200
    
    ;Saved passwords
    cur_x_pos := 500 + offest
    Click %cur_x_pos%, 475
    Sleep, 1200
    
    ;Autofill form data
    cur_x_pos := 500 + offest
    Click %cur_x_pos%, 542
    Sleep, 1200
    
    ;Site settings
    cur_x_pos := 500 + offest
    Click %cur_x_pos%, 612
    Sleep, 1200
    
    ;Media Licenses
    cur_x_pos := 500 + offest
    Click %cur_x_pos%, 680
    Sleep, 1200

    cur_x_pos := 472 + offest
    Click %cur_x_pos%, 946
    Sleep, 1200
}
ClearCache(vm_offest)



;鼠标需要移动到中间位置
Click %tab_x_pos%, 500, 0
Sleep, 1200

;Exit
Exit