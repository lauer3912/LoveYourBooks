CoordMode, Mouse

ads_X_min := 610
ads_X_max := 1100

ClickAds(x_min:=0, x_max:=0, y_min:=0, y_max:=0)
{
    Random, x, %x_min%, %x_max%
    Random, y, %y_min%, %y_max%
    Click %x%, %y%
    Sleep, 2000
}

MoveMouse(max_times:=5, x_min:=0, x_max:=0, y_min:=0, y_max:=0)
{
    Random, loop_times, 2, %max_times%
    Loop, %loop_times%
    {
        Random, x, %x_min%, %x_max%
        Random, y, %y_min%, %y_max%
        Random, sleep_time, 300, 3000

        Click %x%, %y%, 0

        Random, want_click, 0, 10
        if (%want_click% > 5) {
            Click %x%, %y%
        }

        Sleep, %sleep_time%
    }
}

; Active the window
ClickAds(ads_X_min, ads_X_max, 172, 900)
MoveMouse(10, ads_X_min, ads_X_max, 172, 900)


; Click the top ads
ClickAds(ads_X_min, ads_X_max, 172, 215)
MoveMouse(10, ads_X_min, ads_X_max, 172, 900)

; Click the mid ads
ClickAds(ads_X_min, ads_X_max, 534, 720)
MoveMouse(10, ads_X_min, ads_X_max, 172, 900)

; Click the bottom ads
ClickAds(ads_X_min, ads_X_max, 900, 952)
MoveMouse(10, ads_X_min, ads_X_max, 172, 900)

; Exit
;Exit

