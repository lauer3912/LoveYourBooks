CoordMode, Mouse

vpn_x_pos := 1248
vpn_y_pos := 384

btn_connect_x := 1436
btn_connect_y := 918

;启动hi vpn
Click %tab_x_pos%, %tab_y_pos%, 2
Sleep, 15

;启动后, 点击默认连接VPN
Click %btn_connect_x%, %btn_connect_y%
Sleep, 15


; Exit
;Exit

