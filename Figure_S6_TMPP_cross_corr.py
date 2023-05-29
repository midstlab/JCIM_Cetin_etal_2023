from prody import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import os
import fnmatch
from os.path import basename

for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*.pdb'):
        # find the pdb file, parse it, select calphas and parse DCD file on it
        pdb_name = file
        print(pdb_name)
        structure = parsePDB(str(pdb_name))
        file_name_wh_ex = str(os.path.splitext(pdb_name)[0])

        structure_cbeta = structure.select('(protein and name CB) or (name CA and resname GLY) or (resname TMPP and name C4P O4P)')
        residue_number = len(structure_cbeta) 
        ensemble_cov = parseDCD(str(file_name_wh_ex)+".dcd")

        ensemble_cov.setAtoms(structure_cbeta)
        ensemble_cov.setCoords(structure)
        ensemble_cov.superpose()

        print(ensemble_cov)
        eda_ensemble = EDA('')
        eda_ensemble.buildCovariance(ensemble_cov)
        covariance = eda_ensemble.getCovariance()

        cross_corr = np.zeros((residue_number,residue_number))
        for i in range(residue_number):
            for j in range(residue_number):
                a = (3*(i))
                b = (3*(i)+1)
                c = (3*(i)+2)
                d = (3*(j))
                e = (3*(j)+1)
                f = (3*(j)+2)
                cross_corr[i,j] = covariance[a,d]+covariance[b,e]+covariance[c,f]

        corr = cross_corr[0:-2,0:-2]
        print(len(corr))
        file_name_wh_ex = str(os.path.splitext(file)[0])
        fig, ax = plt.subplots()
        #Plot and save cross-corr matrix
        arange = np.arange(residue_number)
        cax = plt.imshow(corr, vmin=-3, vmax=3,extent=[1,159,1,159], cmap=cm.seismic, origin="lower")
        cbar = fig.colorbar(cax, ticks=[-3, 0, 3])
        plt.savefig(str(file_name_wh_ex)+"_correlation", dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()