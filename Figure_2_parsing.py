import alchemlyb
import alchemtest
import alchemlyb.parsing.namd as tweety
import numpy as np
import pandas as pd
from alchemlyb.estimators import MBAR
from alchemlyb.visualisation import plot_convergence
from alchemlyb.visualisation.dF_state import plot_dF_state



#1
u_fw=tweety.extract_u_nk('tmpp_d27e_50ns_fw.fepout',310)
u_bw=tweety.extract_u_nk('tmpp_d27e_50ns_bw.fepout',310)

u_fw.replace(np.nan, 0 , inplace=True)
u_fw[u_fw.isnull().any(axis=1)].fillna(u_bw)
u=u_fw.sort_index(level=u_fw.index.names[1:])

#2
u_fw_100=tweety.extract_u_nk('tmpp_d27e_70ns_fw.fepout',310)
u_bw_100=tweety.extract_u_nk('tmpp_d27e_70ns_bw.fepout',310)

u_fw_100.replace(np.nan, 0 , inplace=True)
u_fw_100[u_fw_100.isnull().any(axis=1)].fillna(u_bw_100)
u_100=u_fw_100.sort_index(level=u_fw_100.index.names[1:])


u_fw_150=tweety.extract_u_nk('tmpp_d27e_100ns_fw.fepout',310)
u_bw_150=tweety.extract_u_nk('tmpp_d27e_100ns_bw.fepout',310)

u_fw_150.replace(np.nan, 0 , inplace=True)
u_fw_150[u_fw_150.isnull()]=u_bw_150
u_150=u_fw_150.sort_index(level=u_fw_150.index.names[1:])

#4

u_fw_200=tweety.extract_u_nk('tmpp_d27e_110ns_fw.fepout',310)
u_bw_200=tweety.extract_u_nk('tmpp_d27e_110ns_bw.fepout',310)

u_fw_200.replace(np.nan, 0 , inplace=True)
u_fw_200[u_fw_200.isnull()]=u_bw_200
u_200=u_fw_200.sort_index(level=u_fw_200.index.names[1:])

#2
u_fw_110=tweety.extract_u_nk('tmpp_d27e_150ns_fw.fepout',310)
u_bw_110=tweety.extract_u_nk('tmpp_d27e_150ns_bw.fepout',310)

u_fw_110.replace(np.nan, 0 , inplace=True)
u_fw_110[u_fw_110.isnull().any(axis=1)].fillna(u_bw_110)
u_110=u_fw_110.sort_index(level=u_fw_110.index.names[1:])


u_fw_70=tweety.extract_u_nk('tmpp_d27e_170ns_fw.fepout',310)
u_bw_70=tweety.extract_u_nk('tmpp_d27e_170ns_bw.fepout',310)

u_fw_70.replace(np.nan, 0 , inplace=True)
u_fw_70[u_fw_70.isnull()]=u_bw_70
u_70=u_fw_70.sort_index(level=u_fw_70.index.names[1:])

#4

u_fw_170=tweety.extract_u_nk('tmpp_d27e_200ns_fw.fepout',310)
u_bw_170=tweety.extract_u_nk('tmpp_d27e_200ns_bw.fepout',310)

u_fw_170.replace(np.nan, 0 , inplace=True)
u_fw_170[u_fw_170.isnull()]=u_bw_170
u_170=u_fw_170.sort_index(level=u_fw_170.index.names[1:])

u_concat = alchemlyb.concat([u,u_70,u_100,u_110,u_150,u_170,u_200])


mbar=MBAR()
mbar.fit(u_concat)

print(mbar.delta_f_.loc['0.00', '1.00'])
print(mbar.d_delta_f_.loc['0.00','1.00'])

from alchemlyb.visualisation import plot_mbar_overlap_matrix
ax = plot_mbar_overlap_matrix(mbar.overlap_matrix)
ax.figure.savefig('O_MBAR.png', bbox_inches='tight', pad_inches=0.0)

forward = []
forward_error = []
backward = []
backward_error = []
num_points = 32

data_list=[u_150,u_200]

for i in range(1, num_points+1):
	# Do the forward
    slice = int(len(data_list[0])/num_points*i)
    u_nk_coul = alchemlyb.concat([data[:slice] for data in data_list])
    estimate = MBAR().fit(u_nk_coul)
    forward.append(estimate.delta_f_.iloc[0,-1])
    forward_error.append(estimate.d_delta_f_.iloc[0,-1])
    # Do the backward
    u_nk_coul = alchemlyb.concat([data[-slice:] for data in data_list])
    estimate = MBAR().fit(u_nk_coul)
    backward.append(estimate.delta_f_.iloc[0,-1])
    backward_error.append(estimate.d_delta_f_.iloc[0,-1])

bx = plot_convergence(forward, forward_error, backward, backward_error)
bx.figure.savefig('dF_t.png')

estimators=[mbar]

fig = plot_dF_state(estimators, orientation='portrait')
fig.savefig('dF_state.png', bbox_inches='tight')





