
proc pow {x y} {
  if {$y 0 =} {
    return 1
  }
  
  set res $x
  for {set i 1} {$i $y <} {incr i} {
    
    set res [expr $res $x *]
  }
  return $res
}

proc calcPi {} {
  set bottom 1
  set sum 0
  for {set i 0} {$i 3 <} {incr i} {
    set ratio [expr 1 $bottom /]
    set sum [expr $sum $ratio +]
    
    puts $sum
  }
}

puts [pow 3 1]