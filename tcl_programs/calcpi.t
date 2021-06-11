
# compute POWER of x to the y
proc pow {x y} {
  if {$y 0 =} {
    return 1
  }
  
  set res $x
  for {set i 1} {$i $y <} {set i [incr $i]} {
    
    set res [expr $res $x *]
  }
  return $res
}

# compute sqrt of n
# this is a poor algorithm for it, it just gets it approximately correct in 10 iterations
proc sqrt {n} {
  # run for 10 iterations
  
  set est 0
  
  set cness 0
  
  for {set i 0} {$i 10 <} {set i [incr $i]} {
    set cness [pow $est 2]
    # negative diff is too high
    # positive diff is too low
    set diff [expr $n $cness -]
    set smalldiff [expr $diff 10 /]
    #puts $smalldiff
    
    set est [expr $est $smalldiff +]
    
    #puts $est
  }
  
  return $est
}

# arctangent of x using the taylor series
proc arctan {x} {
  
  set xsum 0
  set flip 0
  
  for {set i 0} {$i 10 <} {set i [incr $i]} { 
    set pw [expr $i 2 *]
    set pw [expr $pw 1 +]
    
    set xt [pow $x $pw]
    
    set xd [expr $xt $pw /]
    
    if {$flip 0 =} {
      set xsum [expr $xsum $xd +]
      set flip 1
    } {
      set xsum [expr $xsum $xd -]
      set flip 0
    }
    
    #puts $xd
  }
  return $xsum
}

proc decr {x} {
  return [expr $x 1 -]
}

proc incr {x} {
  return [expr $x 1 +]
}

proc factorial {x} {
  set fact 1
  for {} {$x 1 >} {set x [decr $x]} {
    set fact [expr $fact $x *]
  }

  return $fact
}

# get PI
proc PI {} {
  set fr1 [expr 1 5 /]
  set fr1 [arctan $fr1]
  set fr1 [expr $fr1 4 *]
  set fr2 [expr 1 239 /]
  set fr2 [arctan $fr2]
  
  set pi4 [expr $fr1 $fr2 -]
  
  set pi [expr $pi4 4 *]
  
  return $pi
}

proc sin {x} {
  set xsum 0
  set flip 0
  
  for {set i 0} {$i 10 <} {set i [incr $i]} {
    set pw [expr $i 2 *]
    set pw [expr $pw 1 +]
    set fact [factorial $pw]
    
    set xt [pow $x $pw]
    
    set xd [expr $xt $fact /]
    
    if {$flip 0 =} {
      set xsum [expr $xsum $xd +]
      set flip 1
    } {
      set xsum [expr $xsum $xd -]
      set flip 0
    }
    
    #puts $xd
  }
  
  return $xsum
}

proc cos {x} {
  set halfpi [PI]
  set halfpi [expr $halfpi 2 /]
  set sum [expr $halfpi $x +]
  return [sin $sum]
}

proc tan {x} {
  set s [sin $x]
  set c [cos $x]
  
  return [expr $s $c /]
}

puts [tan 2]
