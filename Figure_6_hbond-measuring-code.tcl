   set sel  [atomselect top "resid 303 and not water"]
   set sel2 [atomselect top "protein"]
   set outfile [open d4tmpp-l28r-hbonds.txt w]
   set outfile2 [open d4tmpp2-l28r-hbonds.txt w]

   for {set trajFrame 0} {$trajFrame <= 1001} {incr  trajFrame} {
    $sel frame $trajFrame
    $sel2 frame $trajFrame
	
    set a [measure hbonds 3.2 20.0 $sel $sel2] 
	for {set i 0} {$i <= 2} {incr i} {
	
		set c [lindex $a $i]
		puts $outfile $c 
	}
	#puts $outfile ""
}

for {set trajFrame 0} {$trajFrame <= 1001} {incr  trajFrame} {
    $sel frame $trajFrame
    $sel2 frame $trajFrame
	
    set a [measure hbonds 3.2 20.0 $sel2 $sel] 
	for {set i 0} {$i <= 2} {incr i} {
	
		set c [lindex $a $i]
		puts $outfile2 $c 
	}
	#puts $outfile ""
}
close $outfile
close $outfile2