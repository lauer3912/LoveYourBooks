CoordMode, Mouse

vpn_x_pos := 1248
vpn_y_pos := 384

btn_connect_x := 1436
btn_connect_y := 918

;启动hi vpn
Click %vpn_x_pos%, %vpn_y_pos%, 2
Sleep, 10*1000

;启动后, 点击默认连接VPN
Click %btn_connect_x%, %btn_connect_y%
Sleep, 15*1000
Click %vpn_x_pos%, %vpn_y_pos%, 0


; Exit
Exit
