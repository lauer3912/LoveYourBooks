CoordMode, Mouse
pos_x_min := 20
pos_x_max := 520
pos_y_top := 220
pos_y_bottom := 940

Random, loop_times, 5, 10
Loop, %loop_times%
{
   Random, drag_x, %pos_x_min%, %pos_x_max%

   Random, start_y, %pos_y_bottom% - 20, %pos_y_bottom%
   Random, end_y,   %pos_y_top%, %pos_y_top% + 50

   Random, want_up, 0, 10
   if (%want_up% > 5) {
      MouseClickDrag, L, drag_x, start_y, drag_x, end_y
   } else {
      MouseClickDrag, L, drag_x, end_y, drag_x, start_y
   }

   Random, sleepTime, 1000, 6000
   Sleep, %sleepTime%
}

; Exit
Exit

