CoordMode, Mouse

ads_X_min := 1190
ads_X_max := 1680


ClickAds(x_min:=0, x_max:=0, y_min:=0, y_max:=0)
{
    Random, x, %x_min%, %x_max%
    Random, y, %y_min%, %y_max%
    Click %x%, %y%, 2
    Sleep, 2000
}

; Active the window 
;Click %ads_X_min%, 178


; Click the top ads
ClickAds(ads_X_min, ads_X_max, 172, 215)

; Click the mid ads
ClickAds(ads_X_min, ads_X_max, 534, 720)

; Click the bottom ads
ClickAds(ads_X_min, ads_X_max, 900, 952)

; Exit
;Exit

