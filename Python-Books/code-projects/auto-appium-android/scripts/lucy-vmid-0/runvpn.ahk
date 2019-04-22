CoordMode, Mouse

vpn_x_pos := 88
vpn_y_pos := 384

btn_connect_x := 274
btn_connect_y := 918

desktop_btn_x := 554
desktop_btn_y := 884

;启动hi vpn
Click %vpn_x_pos%, %vpn_y_pos%, 2
Sleep, 15*1000

;启动后, 点击默认连接VPN
Click %btn_connect_x%, %btn_connect_y%
Sleep, 35*1000

;点击显示桌面窗口
Click %desktop_btn_x%, %desktop_btn_y%

;回到hi vpn点
Click %vpn_x_pos%, %vpn_y_pos%, 0


; Exit
Exit

