set nf [molinfo top get numframes]
set outfile [open O3P_O4P_O5P_R52_NH1.dat w]
set outfile2 [open O3P_O4P_O5P_R52_NH2.dat w]
set outfile3 [open O3P_O4P_O5P_S49_O.dat w]
set outfile4 [open O3P_O4P_O5P_M20_N.dat w]
set outfile5 [open O3P_O4P_O5P_N18_O.dat w]
set outfile6 [open O3P_O4P_O5P_W22_O.dat w]	
set outfile7 [open O3P_O4P_O5P_D27_OD1.dat w]
set outfile8 [open O3P_O4P_O5P_D27_OD2.dat w]
		#1
set o3p [atomselect top "resid 303 and name O3P"]
set o4p [atomselect top "resid 303 and name O4P"]
set o5p [atomselect top "resid 303 and name O5P"]
		
		#R52
set r52_nh1 [atomselect top "resid 52 and name NH1"]

set r52_nh2 [atomselect top "resid 52 and name NH2"]

		#S49
set s49 [atomselect top "protein and resid 49 and name O"]
		
		#M20
set m20 [atomselect top "protein and resid 20 and name N"]
		
		#N18
		
set n18 [atomselect top "protein and resid 18 and name O"]
		
		#W22
		
set w22 [atomselect top "protein and resid 22 and name O"]
		
		#D27
		
set d27_od1 [atomselect top "protein and resid 27 and name OD1"]
set d27_od2 [atomselect top "protein and resid 27 and name OD2"]
		
		
		
set o3p_1 [$o3p get index]
set o4p_1 [$o4p get index]
set o5p_1 [$o5p get index]
		
set r52_nh1_1 [$r52_nh1 get index]
set r52_nh2_1 [$r52_nh2 get index]
		
set s49_1 [$s49 get index]
		
set m20_1 [$m20 get index]
		
set n18_1 [$n18 get index]
		
set w22_1 [$w22 get index]
		
set d27_od1_1 [$d27_od1 get index]
set d27_od2_1 [$d27_od2 get index]
		
		#distances measured and written
for {set i 0} {$i<$nf} {incr i} {
		set dist_o3p [measure bond "$r52_nh1_1 $o3p_1"  molid 3 frame $i]
		set dist_o4p [measure bond "$r52_nh1_1 $o4p_1"  molid 3 frame $i] 
		set dist_o5p [measure bond "$r52_nh1_1 $o5p_1"  molid 3 frame $i] 
		
		puts $outfile [format "%8d %8f %8f %8f" $i $dist_o3p $dist_o4p $dist_o5p]
				
}	
	close $outfile
		
for {set i 0} {$i<$nf} {incr i} {
		set dist_o3p_1 [measure bond "$r52_nh2_1 $o3p_1"  molid 3 frame $i]
		set dist_o4p_1 [measure bond "$r52_nh2_1 $o4p_1"  molid 3 frame $i] 
		set dist_o5p_1 [measure bond "$r52_nh2_1 $o5p_1"  molid 3 frame $i] 
		
		puts $outfile2 [format "%8d %8f %8f %8f" $i $dist_o3p_1 $dist_o4p_1 $dist_o5p_1]
		
}	
	close $outfile2
		
for {set i 0} {$i<$nf} {incr i} {
		set dist_o3p_2 [measure bond "$s49_1 $o3p_1"  molid 3 frame $i]
		set dist_o4p_2 [measure bond "$s49_1 $o4p_1"  molid 3 frame $i] 
		set dist_o5p_2 [measure bond "$s49_1 $o5p_1"  molid 3 frame $i] 
		
		puts $outfile3 [format "%8d %8f %8f %8f" $i $dist_o3p_2 $dist_o4p_2 $dist_o5p_2]
		
}	
	close $outfile3
		
for {set i 0} {$i<$nf} {incr i} {
		set dist_o3p_3 [measure bond "$m20_1 $o3p_1"  molid 3 frame $i]
		set dist_o4p_3 [measure bond "$m20_1 $o4p_1"  molid 3 frame $i] 
		set dist_o5p_3 [measure bond "$m20_1 $o5p_1"  molid 3 frame $i] 
		
		puts $outfile4 [format "%8d %8f %8f %8f" $i $dist_o3p_3 $dist_o4p_3 $dist_o5p_3]
		
}	
	close $outfile4
	
for {set i 0} {$i<$nf} {incr i} {
		set dist_o3p_4 [measure bond "$n18_1 $o3p_1"  molid 3 frame $i]
		set dist_o4p_4 [measure bond "$n18_1 $o4p_1"  molid 3 frame $i] 
		set dist_o5p_4 [measure bond "$n18_1 $o5p_1"  molid 3 frame $i] 
		
		puts $outfile5 [format "%8d %8f %8f %8f" $i $dist_o3p_4 $dist_o4p_4 $dist_o5p_4]
		
}	
	close $outfile5
		
for {set i 0} {$i<$nf} {incr i} {
		set dist_o3p_5 [measure bond "$w22_1 $o3p_1"  molid 3 frame $i]
		set dist_o4p_5 [measure bond "$w22_1 $o4p_1"  molid 3 frame $i] 
		set dist_o5p_5 [measure bond "$w22_1 $o5p_1"  molid 3 frame $i] 
		
		puts $outfile6 [format "%8d %8f %8f %8f" $i $dist_o3p_5 $dist_o4p_5 $dist_o5p_5]
		
}	
	close $outfile6
		
for {set i 0} {$i<$nf} {incr i} {
		set dist_o3p_6 [measure bond "$d27_od1_1 $o3p_1"  molid 3 frame $i]
		set dist_o4p_6 [measure bond "$d27_od1_1 $o4p_1"  molid 3 frame $i] 
		set dist_o5p_6 [measure bond "$d27_od1_1 $o5p_1"  molid 3 frame $i] 
		
		puts $outfile7 [format "%8d %8f %8f %8f" $i $dist_o3p_6 $dist_o4p_6 $dist_o5p_6]
		
}	
	close $outfile7
		
		
for {set i 0} {$i<$nf} {incr i} {
		set dist_o3p_7 [measure bond "$d27_od2_1 $o3p_1"  molid 3 frame $i]
		set dist_o4p_7 [measure bond "$d27_od2_1 $o4p_1"  molid 3 frame $i] 
		set dist_o5p_7 [measure bond "$d27_od2_1 $o5p_1"  molid 3 frame $i] 
		
		puts $outfile8 [format "%8d %8f %8f %8f" $i $dist_o3p_7 $dist_o4p_7 $dist_o5p_7]

}	
	close $outfile8