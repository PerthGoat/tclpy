proc buildarr {z} {
  for {set i 0} {$i $z <} {incr i} {
    set x($i) [expr $i 5 +]
  }
  
  return $x
}

proc printArr {a} {
  for {set i 0} {$i 10 <} {incr i} {
    if {$a($i) 11 =} {
      puts "A is $a($i)"
    }
  }
}

set y [buildarr 10]

#puts $y(0)

printArr $y