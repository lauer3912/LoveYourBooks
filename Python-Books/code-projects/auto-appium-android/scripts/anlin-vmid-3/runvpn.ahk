CoordMode, Mouse

vpn_x_pos := 670
vpn_y_pos := 384

btn_connect_x := 860
btn_connect_y := 918

desktop_btn_x := 1132
desktop_btn_y := 884

chrome_x := 760
chrome_y := 196

;启动hi vpn
Click %vpn_x_pos%, %vpn_y_pos%, 2
Sleep, 30*1000

;启动后, 点击默认连接VPN
Click %btn_connect_x%, %btn_connect_y%
Sleep, 35*1000

;点击显示桌面窗口
Click %desktop_btn_x%, %desktop_btn_y%

;回到hi vpn点
Click %vpn_x_pos%, %vpn_y_pos%, 0

;点击Chrome图标
Click %chrome_x%, %chrome_y%, 2

; Exit
Exit

