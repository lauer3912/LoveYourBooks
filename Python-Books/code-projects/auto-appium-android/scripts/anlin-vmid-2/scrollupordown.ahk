CoordMode, Mouse
pos_x_min := 1190
pos_x_max := 1680
pos_y_top := 220
pos_y_bottom := 850


Random, loop_times, 1, 3
Loop, %loop_times%
{
   Random, drag_x, %pos_x_min%, %pos_x_max%
   Random, drag_y, %pos_y_top%, %pos_y_bottom%

   Random, wheel_times, 1, 4

   Loop, %wheel_times%
   {
       Random, want_up, 0, 12
       if (%want_up% > 5) {
          Click WheelUp, %drag_x%, %drag_y%
       } else {
          Click WheelDown, %drag_x%, %drag_y%
       }
   }

   Random, sleep_time, 300, 3000
   Sleep, %sleepTime%
}

; Exit
Exit

