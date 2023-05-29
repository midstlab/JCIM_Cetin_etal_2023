from prody import *
import numpy as np
from os.path import basename
import fnmatch
import os

def config_gen_eq(pdb_name):
	a = str(os.path.splitext(pdb_name)[0])
	file_name_wh_ex = a[0:]
	structure = parsePDB(str(pdb_name))
	
	bf,m,af=a.rpartition('_')
	t=af[:-2]
	
	f = open(str(file_name_wh_ex)+"_eq.conf", 'w')
	f.write("#############################################################\n")
	f.write("## JOB DESCRIPTION                                         ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("#%s Equilibration for FEP Calculation \n\n" % str(file_name_wh_ex))
	f.write("#############################################################\n")
	f.write("## INPUT                                                   ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("set temp                310.0\n")
	f.write("parameters              par_all36_carb.prm\n")
	f.write("parameters              par_all36_cgenff.prm\n")
	f.write("parameters              par_all36_na.prm\n")
	f.write("parameters              par_all36_prot.prm\n")
	f.write("parameters              nadph.prm\n")
	f.write("parameters              na_nad.prm\n")
	f.write("parameters              water_ions.prm\n")
	f.write("parameters              lipid.prm\n")
	f.write("parameters              TMPP.par\n")
	f.write("parameters              D4TMPP.par\n")
	f.write("paraTypeCharmm          on\n")
	f.write("\n")
	f.write("exclude                 scaled1-4\n")
	f.write("1-4scaling              1.0\n")
	f.write("\n")
	f.write("\n")
	f.write("#############################################################\n")
	f.write("## TOPOLOGY & INITIAL CONDITONS                            ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("structure				%s.psf\n" % str(file_name_wh_ex))
	f.write("coordinates		     	%s.pdb\n" % str(file_name_wh_ex))
	f.write("set outputname 		 	%s_eq\n" % str(file_name_wh_ex))
	f.write("temperature             $temp\n")  
	f.write("#############################################################\n")
	f.write("## OUTPUT FREQUENCIES                                      ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("""
outputenergies          200
outputtiming            200
outputpressure          200
restartfreq             200
XSTFreq                 200
dcdfreq					200
""")
	f.write("#############################################################\n")
	f.write("## OUTPUT & RESTART                                        ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("DCDfile					%s_eq.dcd\n" % str(file_name_wh_ex))
	f.write("outputname              $outputname\n")
	f.write("restartname             $outputname\n")
	f.write("""
binaryoutput            yes
binaryrestart           yes

# CONSTANT-T
langevin                on
langevinTemp            $temp
langevinDamping         1.0
""")
	f.write("\n")
	f.write("\n")
	f.write("\n")

	###################
	pdb_atom_coords = structure.getCoords()
	xmax = np.max(pdb_atom_coords[:, 0])
	ymax = np.max(pdb_atom_coords[:, 1])
	zmax = np.max(pdb_atom_coords[:, 2])
	xmin = np.min(pdb_atom_coords[:, 0])
	ymin = np.min(pdb_atom_coords[:, 1])
	zmin = np.min(pdb_atom_coords[:, 2])
	cb_vec1 = abs(xmax-xmin)+0.1
	cb_vec2 = abs(ymax-ymin)+0.1
	cb_vec3 = abs(zmax-zmin)+0.1
	cb_vec1_f = "{0:.1f}".format(cb_vec1)
	cb_vec2_f = "{0:.1f}".format(cb_vec2)
	cb_vec3_f = "{0:.1f}".format(cb_vec3)
	co_x = (xmax+xmin)/2
	co_y = (ymax+ymin)/2
	co_z = (zmax+zmin)/2
	co_x_f = "{0:.1f}".format(co_x)
	co_y_f = "{0:.1f}".format(co_y)
	co_z_f = "{0:.1f}".format(co_z)
	###################
	f.write("# Periodic Boundary Conditions\n")
	f.write("cellBasisVector1     %s      0.0    0.0\n" % cb_vec1_f)
	f.write("cellBasisVector2     0.0       %s   0.0\n" % cb_vec2_f)
	f.write("cellBasisVector3     0.0       0.0    %s\n"% cb_vec3_f)
	f.write("cellOrigin           %s     %s     %s\n" % (co_x_f, co_y_f, co_z_f))
	f.write("\n\n")
	f.write("""# PME

PME                     yes
pmeGridSpacing          1.0
PMETolerance            10e-6
PMEInterpOrder          4
""")
	f.write("\n") 
	f.write("""
# WRAP WATER FOR OUTPUT

wrapAll                 on

# CONSTANT-P

LangevinPiston          on
LangevinPistonTarget    1
LangevinPistonPeriod    100
LangevinPistonDecay     100
LangevinPistonTemp      $temp

StrainRate              0.0 0.0 0.0
useGroupPressure        yes

useFlexibleCell         no

# SPACE PARTITIONING

stepspercycle           10
margin                  1.0

# CUT-OFFS

switching               on
switchdist              11.0
cutoff                  13.0
pairlistdist            15.0


# RESPA PROPAGATOR

timestep                2.0
fullElectFrequency      2
nonbondedFreq           1


# SHAKE

rigidbonds              all
rigidtolerance          0.000001
rigiditerations         400


# COM

ComMotion            no
""")
	f.write("# FEP PARAMETERS\n")
	f.write("\n")
	f.write("\n")
	f.write("source                  fep.tcl\n")
	f.write("alch                    on\n")
	f.write("alchType                FEP\n")
	f.write("alchFile                %s.fep\n" % str(file_name_wh_ex))
	f.write("alchCol                 B\n")
	f.write("alchOutFile             %s_eq.fepout\n" % str(file_name_wh_ex))
	f.write("alchOutFreq             1000\n")
	f.write("\n")
	f.write("""
alchVdwLambdaEnd        1.0
alchElecLambdaStart     0.5
alchVdWShiftCoeff       4.0
alchDecouple            on
""")
	f.write("""
alchEquilSteps          50000
set numSteps            250000

set numMinSteps         500
""")
	f.write("\n")
	
	f.write("runFEPmin 0.0 0.0 0.0 $numSteps $numMinSteps $temp")
	f.close()
	return

def config_gen_eq2(pdb_name):
	a = str(os.path.splitext(pdb_name)[0])
	file_name_wh_ex = a[0:]
	structure = parsePDB(str(pdb_name))
	
	bf,m,af=a.rpartition('_')
	t=af[:-2]
	
	f = open(str(file_name_wh_ex)+"_eq2.conf", 'w')
	f.write("#############################################################\n")
	f.write("## JOB DESCRIPTION                                         ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("#%s Equilibration for FEP Calculation \n\n" % str(file_name_wh_ex))
	f.write("#############################################################\n")
	f.write("## INPUT                                                   ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("set temp                310.0\n")
	f.write("parameters              par_all36_carb.prm\n")
	f.write("parameters              par_all36_cgenff.prm\n")
	f.write("parameters              par_all36_na.prm\n")
	f.write("parameters              par_all36_prot.prm\n")
	f.write("parameters              nadph.prm\n")
	f.write("parameters              na_nad.prm\n")
	f.write("parameters              water_ions.prm\n")
	f.write("parameters              lipid.prm\n")
	f.write("parameters              TMPP.par\n")
	f.write("parameters              D4TMPP.par\n")
	f.write("paraTypeCharmm          on\n")
	f.write("\n")
	f.write("exclude                 scaled1-4\n")
	f.write("1-4scaling              1.0\n")
	f.write("\n")
	f.write("\n")
	f.write("#############################################################\n")
	f.write("## TOPOLOGY & INITIAL CONDITONS                            ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("structure				%s.psf\n" % str(file_name_wh_ex))
	f.write("coordinates		     	%s.pdb\n" % str(file_name_wh_ex))
	f.write("set outputname 		 	%s_eq\n" % str(file_name_wh_ex))
	f.write("bincoordinates 		 	%s_eq.coor\n" % str(file_name_wh_ex))
	f.write("binvelocities   		%s_eq.vel\n" % str(file_name_wh_ex))
	f.write("extendedSystem 		 	%s_eq.xsc\n" % str(file_name_wh_ex))
	f.write("#temperature             $temp\n")  
	f.write("#############################################################\n")
	f.write("## OUTPUT FREQUENCIES                                      ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("""
outputenergies          200
outputtiming            200
outputpressure          200
restartfreq             200
XSTFreq                 200
dcdfreq					200
""")
	f.write("#############################################################\n")
	f.write("## OUTPUT & RESTART                                        ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("DCDfile					%s_eq.dcd\n" % str(file_name_wh_ex))
	f.write("outputname              $outputname\n")
	f.write("restartname             $outputname\n")
	f.write("""
binaryoutput            yes
binaryrestart           yes

# CONSTANT-T
langevin                on
langevinTemp            $temp
langevinDamping         1.0
""")
	f.write("\n")
	f.write("\n")
	f.write("\n")

	###################
	pdb_atom_coords = structure.getCoords()
	xmax = np.max(pdb_atom_coords[:, 0])
	ymax = np.max(pdb_atom_coords[:, 1])
	zmax = np.max(pdb_atom_coords[:, 2])
	xmin = np.min(pdb_atom_coords[:, 0])
	ymin = np.min(pdb_atom_coords[:, 1])
	zmin = np.min(pdb_atom_coords[:, 2])
	cb_vec1 = abs(xmax-xmin)+0.1
	cb_vec2 = abs(ymax-ymin)+0.1
	cb_vec3 = abs(zmax-zmin)+0.1
	cb_vec1_f = "{0:.1f}".format(cb_vec1)
	cb_vec2_f = "{0:.1f}".format(cb_vec2)
	cb_vec3_f = "{0:.1f}".format(cb_vec3)
	co_x = (xmax+xmin)/2
	co_y = (ymax+ymin)/2
	co_z = (zmax+zmin)/2
	co_x_f = "{0:.1f}".format(co_x)
	co_y_f = "{0:.1f}".format(co_y)
	co_z_f = "{0:.1f}".format(co_z)
	###################
	f.write("# Periodic Boundary Conditions\n")
	f.write("cellBasisVector1     %s      0.0    0.0\n" % cb_vec1_f)
	f.write("cellBasisVector2     0.0       %s   0.0\n" % cb_vec2_f)
	f.write("cellBasisVector3     0.0       0.0    %s\n"% cb_vec3_f)
	f.write("cellOrigin           %s     %s     %s\n" % (co_x_f, co_y_f, co_z_f))
	f.write("\n\n")
	f.write("""# PME

PME                     yes
pmeGridSpacing          1.0
PMETolerance            10e-6
PMEInterpOrder          4
""")
	f.write("\n") 
	f.write("""
# WRAP WATER FOR OUTPUT

wrapAll                 on

# CONSTANT-P

LangevinPiston          on
LangevinPistonTarget    1
LangevinPistonPeriod    100
LangevinPistonDecay     100
LangevinPistonTemp      $temp

StrainRate              0.0 0.0 0.0
useGroupPressure        yes

useFlexibleCell         no

# SPACE PARTITIONING

stepspercycle           10
margin                  1.0

# CUT-OFFS

switching               on
switchdist              11.0
cutoff                  13.0
pairlistdist            15.0


# RESPA PROPAGATOR

timestep                2.0
fullElectFrequency      2
nonbondedFreq           1


# SHAKE

rigidbonds              all
rigidtolerance          0.000001
rigiditerations         400


# COM

ComMotion            no
""")
	f.write("# FEP PARAMETERS\n")
	f.write("\n")
	f.write("\n")
	f.write("source                  fep.tcl\n")
	f.write("alch                    on\n")
	f.write("alchType                FEP\n")
	f.write("alchFile                %s.fep\n" % str(file_name_wh_ex))
	f.write("alchCol                 B\n")
	f.write("alchOutFile             %s_eq.fepout\n" % str(file_name_wh_ex))
	f.write("alchOutFreq             1000\n")
	f.write("\n")
	f.write("""
alchVdwLambdaEnd        1.0
alchElecLambdaStart     0.5
alchVdWShiftCoeff       4.0
alchDecouple            on
""")
	f.write("""
alchEquilSteps          50000
set numSteps            250000

set numMinSteps         0
""")
	f.write("\n")
	
	f.write("runFEPmin 0.0 0.0 0.0 $numSteps $numMinSteps $temp")
	f.close()
	return

def config_gen_fw(pdb_name,window_size):
	a = str(os.path.splitext(pdb_name)[0])
	file_name_wh_ex = a[0:]
	structure = parsePDB(str(pdb_name))
	
	bf,m,af=a.rpartition('_')
	t=af[:-2]
	
	f = open(str(file_name_wh_ex)+"_fw.conf", 'w')
	f.write("#############################################################\n")
	f.write("## JOB DESCRIPTION                                         ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("#%s FEP Calculation Forward\n\n" % str(file_name_wh_ex))
	f.write("#############################################################\n")
	f.write("## INPUT                                                   ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("set temp                310.0\n")
	f.write("parameters              par_all36_carb.prm\n")
	f.write("parameters              par_all36_cgenff.prm\n")
	f.write("parameters              par_all36_na.prm\n")
	f.write("parameters              par_all36_prot.prm\n")
	f.write("parameters              nadph.prm\n")
	f.write("parameters              na_nad.prm\n")
	f.write("parameters              water_ions.prm\n")
	f.write("parameters              lipid.prm\n")
	f.write("parameters              TMPP.par\n")
	f.write("parameters              D4TMPP.par\n")
	f.write("paraTypeCharmm          on\n")
	f.write("\n")
	f.write("exclude                 scaled1-4\n")
	f.write("1-4scaling              1.0\n")
	f.write("\n")
	f.write("\n")
	f.write("#############################################################\n")
	f.write("## TOPOLOGY & INITIAL CONDITONS                            ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("structure				%s.psf\n" % str(file_name_wh_ex))
	f.write("coordinates		     	%s.pdb\n" % str(file_name_wh_ex))
	f.write("set outputname 		 	%s_fw\n" % str(file_name_wh_ex))
	f.write("bincoordinates          %s_eq.coor\n" % str(file_name_wh_ex))  
	f.write("binvelocities           %s_eq.vel\n" % str(file_name_wh_ex)) 
	f.write("extendedsystem          %s_eq.xsc\n" % str(file_name_wh_ex)) 
	f.write("#############################################################\n")
	f.write("## OUTPUT FREQUENCIES                                      ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("""
outputenergies          1000
outputtiming            1000
outputpressure          1000
restartfreq             1000
XSTFreq                 1000
dcdfreq					1000
""")
	f.write("#############################################################\n")
	f.write("## OUTPUT & RESTART                                        ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("DCDfile					%s_fw.dcd\n" % str(file_name_wh_ex))
	f.write("outputname              $outputname\n")
	f.write("restartname             $outputname\n")
	f.write("""
binaryoutput            yes
binaryrestart           yes

# CONSTANT-T
langevin                on
langevinTemp            $temp
langevinDamping         1.0
""")
	f.write("\n")
	f.write("\n")
	f.write("\n")

	###################
	pdb_atom_coords = structure.getCoords()
	xmax = np.max(pdb_atom_coords[:, 0])
	ymax = np.max(pdb_atom_coords[:, 1])
	zmax = np.max(pdb_atom_coords[:, 2])
	xmin = np.min(pdb_atom_coords[:, 0])
	ymin = np.min(pdb_atom_coords[:, 1])
	zmin = np.min(pdb_atom_coords[:, 2])
	cb_vec1 = abs(xmax-xmin)+0.1
	cb_vec2 = abs(ymax-ymin)+0.1
	cb_vec3 = abs(zmax-zmin)+0.1
	cb_vec1_f = "{0:.1f}".format(cb_vec1)
	cb_vec2_f = "{0:.1f}".format(cb_vec2)
	cb_vec3_f = "{0:.1f}".format(cb_vec3)
	co_x = (xmax+xmin)/2
	co_y = (ymax+ymin)/2
	co_z = (zmax+zmin)/2
	co_x_f = "{0:.1f}".format(co_x)
	co_y_f = "{0:.1f}".format(co_y)
	co_z_f = "{0:.1f}".format(co_z)
	###################
	f.write("# Periodic Boundary Conditions\n")
	f.write("cellBasisVector1     %s      0.0    0.0\n" % cb_vec1_f)
	f.write("cellBasisVector2     0.0       %s   0.0\n" % cb_vec2_f)
	f.write("cellBasisVector3     0.0       0.0    %s\n"% cb_vec3_f)
	f.write("cellOrigin           %s     %s     %s\n" % (co_x_f, co_y_f, co_z_f))
	f.write("\n\n")
	f.write("""# PME

PME                     yes
pmeGridSpacing          1.0
PMETolerance            10e-6
PMEInterpOrder          4
""")
	f.write("\n")
	f.write("""
# WRAP WATER FOR OUTPUT

wrapAll                 on

# CONSTANT-P

LangevinPiston          on
LangevinPistonTarget    1
LangevinPistonPeriod    100
LangevinPistonDecay     100
LangevinPistonTemp      $temp

StrainRate              0.0 0.0 0.0
useGroupPressure        yes

useFlexibleCell         no

# SPACE PARTITIONING

stepspercycle           10
margin                  1.0

# CUT-OFFS

switching               on
switchdist              11.0
cutoff                  13.0
pairlistdist            15.0


# RESPA PROPAGATOR

timestep                2.0
fullElectFrequency      2
nonbondedFreq           1


# SHAKE

rigidbonds              all
rigidtolerance          0.000001
rigiditerations         400


# COM

ComMotion            no
""")
	f.write("# FEP PARAMETERS\n")
	f.write("\n")
	f.write("\n")
	f.write("source                  fep.tcl\n")
	f.write("alch                    on\n")
	f.write("alchType                FEP\n")
	f.write("alchFile                %s.fep\n" % str(file_name_wh_ex))
	f.write("alchCol                 B\n")
	f.write("alchOutFile             %s_fw.fepout\n" % str(file_name_wh_ex))
	f.write("alchOutFreq             1000\n")
	f.write("\n")
	f.write("""
alchVdwLambdaEnd        1.0
alchElecLambdaStart     0.5
alchVdWShiftCoeff       4.0
alchDecouple            on
""")
	f.write("""
alchEquilSteps          50000
set numSteps            100000
""")
	f.write("\n")
	delta_lambda=1/window_size
	f.write("set dLambda             %s\n" % str(delta_lambda))
	f.write("\n")
	f.write("runFEP 0.0 1.0 $dLambda $numSteps" )
	f.close()
	return

def config_gen_bw(pdb_name,window_size):
	a = str(os.path.splitext(pdb_name)[0])
	file_name_wh_ex = a[0:]
	structure = parsePDB(str(pdb_name))
	
	bf,m,af=a.rpartition('_')
	t=af[:-2]
	
	f = open(str(file_name_wh_ex)+"_bw.conf", 'w')
	f.write("#############################################################\n")
	f.write("## JOB DESCRIPTION                                         ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("#%s Backward FEP Calculation \n\n" % str(file_name_wh_ex))
	f.write("#############################################################\n")
	f.write("## INPUT                                                   ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("set temp                310.0\n")
	f.write("parameters              par_all36_carb.prm\n")
	f.write("parameters              par_all36_cgenff.prm\n")
	f.write("parameters              par_all36_na.prm\n")
	f.write("parameters              par_all36_prot.prm\n")
	f.write("parameters              nadph.prm\n")
	f.write("parameters              na_nad.prm\n")
	f.write("parameters              water_ions.prm\n")
	f.write("parameters              lipid.prm\n")
	f.write("parameters              TMPP.par\n")
	f.write("parameters              D4TMPP.par\n")
	f.write("paraTypeCharmm          on\n")
	f.write("\n")
	f.write("exclude                 scaled1-4\n")
	f.write("1-4scaling              1.0\n")
	f.write("\n")
	f.write("\n")
	f.write("#############################################################\n")
	f.write("## TOPOLOGY & INITIAL CONDITONS                            ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("structure				%s.psf\n" % str(file_name_wh_ex))
	f.write("coordinates		     	%s.pdb\n" % str(file_name_wh_ex))
	f.write("set outputname 		 	%s_bw\n" % str(file_name_wh_ex))
	f.write("bincoordinates          %s_fw.coor\n" % str(file_name_wh_ex))  
	f.write("binvelocities           %s_fw.vel\n" % str(file_name_wh_ex)) 
	f.write("extendedsystem          %s_fw.xsc\n" % str(file_name_wh_ex)) 
	f.write("#############################################################\n")
	f.write("## OUTPUT FREQUENCIES                                      ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("""
outputenergies          1000
outputtiming            1000
outputpressure          1000
restartfreq             1000
XSTFreq                 1000
dcdfreq					1000
""")
	f.write("#############################################################\n")
	f.write("## OUTPUT & RESTART                                        ##\n")
	f.write("#############################################################\n")
	f.write("\n")
	f.write("DCDfile					%s_bw.dcd\n" % str(file_name_wh_ex))
	f.write("outputname              $outputname\n")
	f.write("restartname             $outputname\n")
	f.write("""
binaryoutput            yes
binaryrestart           yes

# CONSTANT-T
langevin                on
langevinTemp            $temp
langevinDamping         1.0
""")
	f.write("\n")
	f.write("\n")
	f.write("\n")

	###################
	pdb_atom_coords = structure.getCoords()
	xmax = np.max(pdb_atom_coords[:, 0])
	ymax = np.max(pdb_atom_coords[:, 1])
	zmax = np.max(pdb_atom_coords[:, 2])
	xmin = np.min(pdb_atom_coords[:, 0])
	ymin = np.min(pdb_atom_coords[:, 1])
	zmin = np.min(pdb_atom_coords[:, 2])
	cb_vec1 = abs(xmax-xmin)+0.1
	cb_vec2 = abs(ymax-ymin)+0.1
	cb_vec3 = abs(zmax-zmin)+0.1
	cb_vec1_f = "{0:.1f}".format(cb_vec1)
	cb_vec2_f = "{0:.1f}".format(cb_vec2)
	cb_vec3_f = "{0:.1f}".format(cb_vec3)
	co_x = (xmax+xmin)/2
	co_y = (ymax+ymin)/2
	co_z = (zmax+zmin)/2
	co_x_f = "{0:.1f}".format(co_x)
	co_y_f = "{0:.1f}".format(co_y)
	co_z_f = "{0:.1f}".format(co_z)
	###################
	f.write("# Periodic Boundary Conditions\n")
	f.write("cellBasisVector1     %s      0.0    0.0\n" % cb_vec1_f)
	f.write("cellBasisVector2     0.0       %s   0.0\n" % cb_vec2_f)
	f.write("cellBasisVector3     0.0       0.0    %s\n"% cb_vec3_f)
	f.write("cellOrigin           %s     %s     %s\n" % (co_x_f, co_y_f, co_z_f))
	f.write("\n\n")
	f.write("""# PME

PME                     yes
pmeGridSpacing          1.0
PMETolerance            10e-6
PMEInterpOrder          4
""")
	f.write("\n")
	f.write("""
# WRAP WATER FOR OUTPUT

wrapAll                 on

# CONSTANT-P

LangevinPiston          on
LangevinPistonTarget    1
LangevinPistonPeriod    100
LangevinPistonDecay     100
LangevinPistonTemp      $temp

StrainRate              0.0 0.0 0.0
useGroupPressure        yes

useFlexibleCell         no

# SPACE PARTITIONING

stepspercycle           10
margin                  1.0

# CUT-OFFS

switching               on
switchdist              11.0
cutoff                  13.0
pairlistdist            15.0


# RESPA PROPAGATOR

timestep                2.0
fullElectFrequency      2
nonbondedFreq           1


# SHAKE

rigidbonds              all
rigidtolerance          0.000001
rigiditerations         400


# COM

ComMotion            no
""")
	f.write("# FEP PARAMETERS\n")
	f.write("\n")
	f.write("\n")
	f.write("source                  fep.tcl\n")
	f.write("alch                    on\n")
	f.write("alchType                FEP\n")
	f.write("alchFile                %s.fep\n" % str(file_name_wh_ex))
	f.write("alchCol                 B\n")
	f.write("alchOutFile             %s_bw.fepout\n" % str(file_name_wh_ex))
	f.write("alchOutFreq             1000\n")
	f.write("\n")
	f.write("""
alchVdwLambdaEnd        1.0
alchElecLambdaStart     0.5
alchVdWShiftCoeff       4.0
alchDecouple            on
""")
	f.write("""
alchEquilSteps          50000
set numSteps            100000
""")
	f.write("\n")
	delta_lambda= -1/window_size
	f.write("set dLambda             %s\n" % str(delta_lambda))
	f.write("\n")
	f.write("runFEP 1.0 0.0 $dLambda $numSteps")
	f.close()
	return
	
pdbname = input("What is the pdb name:")
w_size = int(input("How many is the number of windows:"))


config_gen_eq(pdbname)
config_gen_eq2(pdbname)
config_gen_fw(pdbname,w_size)
config_gen_bw(pdbname,w_size)