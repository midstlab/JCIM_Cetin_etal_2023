set pro [atomselect top "protein"]
set dhf [atomselect top "resid 300 and not water"]

set ind1 [$pro get index]
set ind2 [$dhf get index]

set ind [concat $ind1 $ind2]
#set ind [lremove $ind3 0]
set outfile [open tmpp-wt-index.dat w] 

set b [llength $ind]

for {set i 0} {$i < $b} {incr i} {

set a [atomselect top "index [lindex $ind $i]"]
set d [atomselect top "index [lindex $ind $i]"]
set c [atomselect top "index [lindex $ind $i]"]

 set resn [ $a get resname]
 set resi [ $d get resid]
 set nm   [ $c get name]
 
 set str [format "%1d %3s%1d %1s" [lindex $ind $i] $resn $resi $nm]
 
 join $str ""
 
 puts $outfile $str

}

close $outfile