from prody import *
import numpy as np
from numpy import cross, eye, dot
from scipy.linalg import expm, norm
from os.path import basename
import math
import fnmatch
import os

#infile = input("what is pdb file name : ")
infile='WTtmppf550.pdb'
outfile = str(os.path.splitext(infile)[0])
structure=parsePDB(str(infile))
atom_selection_string="name C4P O4P C5P and resname TMPP"
structure_TMPP = structure.select(atom_selection_string)

coord=structure_TMPP.getCoords()
print(coord)
r21=coord[2]-coord[0]#C5P-C4P
r23=coord[1]-coord[0]#O4P-C5P
r13=coord[1]-coord[2]#O4P-C4P

bond=0.96

theta123=math.acos(np.inner(r21,r23)/(np.linalg.norm(r21)*np.linalg.norm(r23)))
theta234=math.radians(80)

theta0=math.radians(180)
alpha= theta123+theta234-theta0

n1=np.cross(r13,-r21)

M=np.array([[n1[0],n1[1],n1[2]],
            [coord[1][0]-coord[0][0],coord[1][1]-coord[0][1],coord[1][2]-coord[0][2]],
            [coord[0][0]-coord[2][0],coord[0][1]-coord[2][1],coord[0][2]-coord[2][2]]])

vector=np.array([np.inner(n1,coord[2]),-math.cos(theta234)*bond*np.linalg.norm(r23)+np.inner(coord[1],coord[1])-np.inner(coord[1],coord[0]), np.inner(coord[1],-r21)-bond*np.linalg.norm(r21)*math.cos(alpha)])
invM=np.linalg.inv(M)

r4=np.dot(invM,vector)
x=round(r4[0],3)
y=round(r4[1],3)
z=round(r4[2],3)

print(r4)

coord3=[x,y,z]
		
template='TMPP'
mutation='T2D4'

a = []
n=0
with open("T2D4template.pdb", "r") as f:
	for line2 in f:
		if str(mutation) in line2 : 
			a.append(line2)
tmpp =[]

with open(infile,'r') as c:
	for line in c:
		if str(template) in line:
			tmpp.append(line)
#needs to be changed for D3TMPP
d4tmpp=[]
for i in range(len(tmpp)):
	if str('C9') in tmpp[i]:
		continue
	elif str('H91') in tmpp[i]:
		continue
	elif str('H92') in tmpp[i]:
		continue
	elif str('H93') in tmpp[i]:
		continue
	else:
		d4tmpp.append(tmpp[i])

new_d4tmpp=[]
#adding hydrogen -- needs to be changed for D3TMPP
for i in range(len(d4tmpp)):
	if str('O4P') in d4tmpp[i]:
		new_d4tmpp.append(d4tmpp[i])
		new_d4tmpp.append(str('ATOM   2592  H4P TMPPO 300      ')+str(coord3[0])+str('  ')+str(coord3[1])+str('  ')+str(float(coord3[2]))+str(d4tmpp[i][54:]))
	else:
		new_d4tmpp.append(d4tmpp[i])

j=0
k=0
for i in range(len(a)):
	if i<40:
		a[i]=a[i][0:31]+' '+tmpp[j][32:54]+a[i][54:]
		j=j+1
	elif i>=39 and i<len(a):
		a[i]=a[i][0:31]+' '+new_d4tmpp[k][32:54]+a[i][54:]
		k=k+1

with open("%s_final.pdb" % outfile,"w") as g:
	with open( infile,"r") as b:
		for line in b:
			if str(template) and str('NA2') in line:
				for i in range(len(a)):
					g.write(a[i])
			elif str(template) in line:
				continue
			else : 
				g.write(line)




