CoordMode, Mouse
pos_x_min := 20
pos_x_max := 520
pos_y_top := 220
pos_y_bottom := 940

Random, loop_times, 2, 10
Loop, %loop_times%
{
   Random, drag_x, %pos_x_min%, %pos_x_max%
   Random, drag_y, %pos_y_top%, %pos_y_bottom%
   Random, want_up, 0, 10
   Random, wheel_times, 1, 5
   
   Loop, %wheel_times%
   {
       if (%want_up% > 5) {
          Click WheelUp, %drag_x%, %drag_y%
       } else {
          Click WheelDown, %drag_x%, %drag_y%
       }
   }

   Random, sleep_time, 1000, 3000
   Sleep, %sleepTime%
}

; Exit
Exit

