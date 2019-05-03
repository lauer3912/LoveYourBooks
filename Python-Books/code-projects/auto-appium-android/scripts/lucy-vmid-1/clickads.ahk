CoordMode, Mouse

ads_X_min := 610
ads_X_max := 1100

ClickAds(x_min:=0, x_max:=0, y_min:=0, y_max:=0)
{
    Random, x, %x_min%, %x_max%
    Random, y, %y_min%, %y_max%
    Click %x%, %y%
    Random, sleep_time, 300, 3000
    Sleep, %sleep_time%
}

MoveMouse(max_times:=20, x_min:=0, x_max:=0, y_min:=0, y_max:=0)
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

Loop, 3 {
    Random, best_index, 1, 7
    Sleep, 2*1000
    if (%best_index% >= 5) {
        ; Active the window
        ClickAds(ads_X_min, ads_X_max, 172, 850)
        MoveMouse(2, ads_X_min, ads_X_max, 172, 850)
    }
    Sleep, 2*1000
    if (%best_index% >= 4) {

        ; Click the top ads
        ClickAds(ads_X_min, ads_X_max, 172, 215)
        MoveMouse(2, ads_X_min, ads_X_max, 172, 850)
    }
    Sleep, 2*1000
    if (%best_index% >= 3) {
        ; Click the mid ads
        ClickAds(ads_X_min, ads_X_max, 534, 720)
        MoveMouse(2, ads_X_min, ads_X_max, 172, 850)
    }
    Sleep, 2*1000
    if (%best_index% >= 2) {
        ; Click the bottom ads
        ClickAds(ads_X_min, ads_X_max, 800, 850)
        MoveMouse(2, ads_X_min, ads_X_max, 172, 850)
    } else {
        MoveMouse(2, ads_X_min, ads_X_max, 172, 850)
    }
}

; Click the top ads
ClickAds(ads_X_min, ads_X_max, 172, 215)
MoveMouse(10, ads_X_min, ads_X_max, 172, 850)

; Click the mid ads
ClickAds(ads_X_min, ads_X_max, 534, 720)
MoveMouse(10, ads_X_min, ads_X_max, 172, 850)

; Click the bottom ads
ClickAds(ads_X_min, ads_X_max, 800, 850)
MoveMouse(10, ads_X_min, ads_X_max, 172, 850)



; Exit
Exit

