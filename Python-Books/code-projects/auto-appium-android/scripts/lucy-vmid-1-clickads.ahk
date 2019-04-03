CoordMode, Mouse

ads_X_min := 610
ads_X_max := 1100


ClickAds(x_min:=0, x_max:=0, y_min:=0, y_max:=0)
{
    Random, x, %x_min%, %x_max%
    Random, y, %y_min%, %y_max%
    Click %x%, %y%
    Sleep, 3000
}

WheelUpOrDown()
{
    Random, times, 5, 12
    Loop %times%
        Random, flag, 0, 1
        if (%flag% > 0 ) {
            Click WheelDown
        } else {
            Click WheelUp
        }
}

; Active the window 
Click %ads_X_min%, 178

; Click the top ads
ClickAds(ads_X_min, ads_X_max, 172, 215)

; Click the mid ads
ClickAds(ads_X_min, ads_X_max, 534, 720)

; Click the bottom ads
ClickAds(ads_X_min, ads_X_max, 900, 952)

; WheelUp or WheelDown
;WheelUpOrDown()

; Exit
;Exit

