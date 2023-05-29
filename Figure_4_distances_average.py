from collections import defaultdict
from collections import OrderedDict
import matplotlib.pyplot as plt 
import itertools
import numpy as np
import os

for file in os.listdir():
	file_name_wh_ex = str(os.path.splitext(file)[0])
	o3p=[]
	o4p=[]
	o4p=[]

	with open(file) as g:
		for line in g:
			line=line.split(' ')
			o3p.append(line[1])
			o4p.append(line[2])
			o5p.append(line[3])

	average_o3p=np.average(o3p)
	average_o4p=np.average(o4p)
	average_o5p=np.average(o5p)

	std_o3p=np.std(o3p)
	std_o4p=np.std(o4p)
	std_o5p=np.std(o5p)

	wtc_file=str(file_name_wh_ex)+".txt"
	with open(wtc_file,'w') as f:
        f.write('Average & STD:    %s %s %s %s %s %s\n' % (average_o3p,average_o4p,average_o5p,std_o4p,std_o4p,std_o5p))