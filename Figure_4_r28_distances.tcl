set nf [molinfo top get numframes]
set outfile [open O3P_O4P_O5P_R28_NH1.dat w]
set outfile2 [open O3P_O4P_O5P_R28_NH2.dat w]
set outfile3 [open O3P_O4P_O5P_R28_NE.dat w]

		#1
set o3p [atomselect top "resid 300 and name O3P"]
set o4p [atomselect top "resid 300 and name O4P"]
set o5p [atomselect top "resid 300 and name O5P"]
		
		#28
set r28_nh1 [atomselect top "resid 28 and name NH1"]

set r28_nh2 [atomselect top "resid 28 and name NH2"]

		#NE
set r28_ne [atomselect top "protein and resid 28 and name NE"]
		
		
		
set o3p_1 [$o3p get index]
set o4p_1 [$o4p get index]
set o5p_1 [$o5p get index]
		
set r28_nh1_1 [$r28_nh1 get index]
set r28_nh2_1 [$r28_nh2 get index]
set r28_ne_1 [$r28_ne get index]
		
		
		#distances measured and written
for {set i 0} {$i<$nf} {incr i} {
		set dist_o3p [measure bond "$r28_nh1_1 $o3p_1"  molid 4 frame $i]
		set dist_o4p [measure bond "$r28_nh1_1 $o4p_1"  molid 4 frame $i] 
		set dist_o5p [measure bond "$r28_nh1_1 $o5p_1"  molid 4 frame $i] 
		
		puts $outfile [format "%8d %8f %8f %8f" $i $dist_o3p $dist_o4p $dist_o5p]
				
}	
	close $outfile
		
for {set i 0} {$i<$nf} {incr i} {
		set dist_o3p_1 [measure bond "$r28_nh2_1 $o3p_1"  molid 4 frame $i]
		set dist_o4p_1 [measure bond "$r28_nh2_1 $o4p_1"  molid 4 frame $i] 
		set dist_o5p_1 [measure bond "$r28_nh2_1 $o5p_1"  molid 4 frame $i] 
		
		puts $outfile2 [format "%8d %8f %8f %8f" $i $dist_o3p_1 $dist_o4p_1 $dist_o5p_1]
		
}	
	close $outfile2
		
for {set i 0} {$i<$nf} {incr i} {
		set dist_o3p_2 [measure bond "$r28_ne_1 $o3p_1"  molid 4 frame $i]
		set dist_o4p_2 [measure bond "$r28_ne_1 $o4p_1"  molid 4 frame $i] 
		set dist_o5p_2 [measure bond "$r28_ne_1 $o5p_1"  molid 4 frame $i] 
		
		puts $outfile3 [format "%8d %8f %8f %8f" $i $dist_o3p_2 $dist_o4p_2 $dist_o5p_2]
		
}	
	close $outfile3
		