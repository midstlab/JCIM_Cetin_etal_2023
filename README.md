# JCIM_codes
Codes used in "Kinetic barrier to enzyme inhibition is manipulated by dynamical local interactions in E. coli DHFR" paper

All datasets are accessible from zenodo.org under the paper name. 

# Figure 2

for creating dual structure pdb file use pdb_prep.py
for creating configuration files use config.py
for the calculation of energy estimates use parsing.py 

# Figure 4

Codes for extracting timewise distance information. Use it after aligning the structure. 

for tcl: source codename.tcl
for python : for each system (active site residues for WT and L28R) make sperate folder for each and place the python code inside. The code will be calculating the averages and standard deviations for the system.

          Dataset :
          tmpp-WT.dcd, tmpp-L28R.dcd, d4tmpp-WT.dcd, d4tmpp-L28R.dcd 
          stride 500, 1 microsecond each
          
# Figure 6

Timewise barcode graphs.

hbond_measuring_code : source the file. It will extract the timewise hydrogen bonding profile of the ligand with the protein. 
index_extraction : source the file. It will extract the index ids used in hbond_measuring_code for each atoms of protein and the ligand. 
occupancy&barcode : after having the outputs of hbond_measuring_code & index_extraction scripts run the file for occupancy first. Then from the listed occupancies if you like to extract barcode information uncomment barcode line in the script. Use the occupancy naming and numbering as it exemplified in the script.

          Dataset:
          tmpp-WT.dcd, tmpp-L28R.dcd, d4tmpp-WT.dcd, d4tmpp-L28R.dcd 
          stride 500, 1 microsecond each

# Figure 8

Hydrogen bonding information and their difference from the wild-type system.

First extract hbond data from the VMD Timeline Plugin. Use index_extraction to get the protein indexes.

Give 2 files as input to hydrogen_bond_enzyme.py. Note that you have to have 5 pairs of these files since the microsecond trajectory is chopped to five. In wt_occ, the program will calculate the avegare occupancy of these five chunks for each hydrogen bonding and compare it with the target system.

Run the to code for 0 difference in line 185 to get the difference information. You may run a frequency distribution analysis elsewhere to calculate how many sigma defines your treshold. Then you can change line 185 to this number to get the only significant hydrogen bonding information. 

          Dataset:
          tmpp-WT-1.dcd, tmpp-WT-2.dcd, tmpp-WT-3.dcd, tmpp-WT-4.dcd, tmpp-WT-5.dcd, corresponding psf file : tmpp-WT-pro.psf
          tmpp-L28R-1.dcd, tmpp-L28R-2.dcd, tmpp-L28R-3.dcd, tmpp-L28R-4.dcd, tmpp-L28R-5.dcd, corresponding psf file : tmpp-L28R-pro.psf
          d4tmpp-WT-1.dcd, d4tmpp-WT-2.dcd, d4tmpp-WT-3.dcd, d4tmpp-WT-4.dcd, d4tmpp-WT-5.dcd, corresponding psf file : d4tmpp-WT-pro.psf
          d4tmpp-L28R-1.dcd, d4tmpp-L28R-2.dcd, d4tmpp-L28R-3.dcd, d4tmpp-L28R-4.dcd, d4tmpp-L28R-5.dcd, corresponding psf file : d4tmpp-L28R-pro.psf
          
          stride 100, 1 microsecond chopped into five
          
# Figure S4

Root mean squeared fluctuations (RMSF).

source rmsf.tcl to get the RMSF values.

          Dataset:
          tmpp-WT-1.dcd, tmpp-WT-2.dcd, tmpp-WT-3.dcd, tmpp-WT-4.dcd, tmpp-WT-5.dcd, corresponding psf file : tmpp-WT-pro.psf
          tmpp-L28R-1.dcd, tmpp-L28R-2.dcd, tmpp-L28R-3.dcd, tmpp-L28R-4.dcd, tmpp-L28R-5.dcd, corresponding psf file : tmpp-L28R-pro.psf
          d4tmpp-WT-1.dcd, d4tmpp-WT-2.dcd, d4tmpp-WT-3.dcd, d4tmpp-WT-4.dcd, d4tmpp-WT-5.dcd, corresponding psf file : d4tmpp-WT-pro.psf
          d4tmpp-L28R-1.dcd, d4tmpp-L28R-2.dcd, d4tmpp-L28R-3.dcd, d4tmpp-L28R-4.dcd, d4tmpp-L28R-5.dcd, corresponding psf file : d4tmpp-L28R-pro.psf
          
          stride 100, 1 microsecond chopped into five

# Figure S6

Cross-correlation maps.

Make different folders for each ligand. Place the the mutant systems (pdb and dcd files) to this folder (WT and L28R in this case). Then place the cross_corr (cross correlation) code for corresponding ligand into the that folder. The code will generate cross-correlation images for the systems you placed into.

          Dataset:
          tmpp-WT.dcd, tmpp-L28R.dcd, d4tmpp-WT.dcd, d4tmpp-L28R.dcd 
          stride 500, 1 microsecond each
