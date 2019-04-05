CoordMode, Mouse
pos_x_min := 610
pos_x_max := 1100
pos_y_top := 220
pos_y_bottom := 940

Random, loop_times, 5, 15
Loop, %loop_times%
{
   Random, drag_x, %pos_x_min%, %pos_x_max%
   Random, drag_y, %pos_y_top%, %pos_y_bottom%
   Random, want_up, 0, 10
   Random, wheel_times, 1, 12

   Loop, %wheel_times%
   {
      Click WheelDown, %drag_x%, %drag_y%
   }

   Random, sleepTime, 300, 3000
   Sleep, %sleepTime%
}

; Exit
Exit

