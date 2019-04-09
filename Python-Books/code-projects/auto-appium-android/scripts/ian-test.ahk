CoordMode, Mouse

ads_X_min := 2660
ads_X_max := 2988


ClickAds(x_min, x_max, y_min, y_max)
{
    Random, x, x_min, x_max
    Random, y, y_min, y_max
    Click x, y
    Sleep, 3000
}

; Active the window 
Click ads_X_min, 500


; Click the top ads
ClickAds(ads_X_min, ads_X_max, 172, 215)


; Click the mid ads
ClickAds(ads_X_min, ads_X_max, 534, 720)


; Click the bottom ads
ClickAds(ads_X_min, ads_X_max, 800, 850)
