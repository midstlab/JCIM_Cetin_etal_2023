from collections import defaultdict
from collections import OrderedDict
import matplotlib.pyplot as plt 
import itertools
import numpy as np
from numpy import array

index_file='d4tmpp-l28r'
file='d4tmpp-l28r'


def data_input(file,index_file):
	index={}
	    #index list from VMD 1207 -- DHF161 NH 1130 -- ARG28 NE 
	with open(str(index_file)+'-index.dat') as f:
	    for line in f:
	    	line=line.split(' ')
	    	index[line[0]]=[line[1],line[2][0:-1]]
	with open(str(file)+'-hbonds.txt') as g:

	    #file_lines = [line[:-1] for line in g if line.strip() != '']
	    mat_raw=[[float(term) for term in line.split()] for line in g]
	    mat=np.array(mat_raw,list)
	length=[]
	#print(mat[3005])
	for i in range(len(mat)-1):
		#print(mat[i])
		#print(len(mat[i]))
		#print(i)
		if mat[i]==[]:
			length.append(0)
		else:
			length.append(len(mat[i]))

	#print(len(mat))
	columns={}
	for i in range(max(length)):
		columns[i]=np.zeros((int(len(mat)/3),3),list)

	
	mat=np.array(mat)
	mat=np.transpose(mat)

	#print(mat)
	j=0
	while j < max(length):
		count=0
		#print(len(mat))
		for i in range(0,(len(mat)),3):
			if count < len(mat):
				#print(count)
				#print(mat[i],mat[i+1],mat[i+2])
				#print(j)
				if not mat[i]:
					#print(mat[i])
					columns[j][count]=[0,0,0]
					count+=1
				elif len(mat[i]) < j+1:
					continue
				else:
					columns[j][count]=[mat[i][j],mat[i+1][j],mat[i+2][j]]
				#print(columns[j][count])
					#print(count)
					count+=1
		j=j+1

	for x in columns:
		columns[x].sort()
	#print(first_column)
	#print(len(columns[1]))
	#print(len(columns[0]))
	size=int(len(mat)/3)
	#print(size)

	#print(type(columns))
	keys_list={}
	for keys,vals in columns.items():
		for i in range(len(columns[keys])):
				keys_list[tuple(vals[i])]=np.zeros((int(len(mat)/3),1),int)

	

	for keys,vals in columns.items():
		
		print(columns[keys][0])
		for leys,lays in keys_list.items():
			
			for i in range(len(columns[keys])):
				if tuple(columns[keys][i]) == leys:
					lays[i]=1

					
					
		#print(len(lays))
	
	res={}	
	res_old={}
	for key,value in keys_list.items():
			#print(hbond_index.get(key)[1])
			#0: [2580.0, 86.0, 2582.0]
		d=key[0]


		
		
		d=str(int(d))
		donor=index.get(d)
		
		a=key[2]
		a=str(int(a))
		acceptor=index.get(a)

		
		if donor==None or acceptor==None:
			print('Your index file has some missing atoms.')
			continue
		else:
		    mat_key=(donor[0],donor[1],acceptor[0],acceptor[1])

		if mat_key in res:
			for i in range(len(value)):
				if res_old[mat_key][i]==1:
					res[mat_key][i]=1
				
		else:
			res[mat_key]=value
			res_old[mat_key]=value
			#print(mat_key)
			#print(sum(value)/size*100)

		

		
	#print(res)
	final={}

	for key,val in res.items():
		#print(key)
		string = (key[0],key[2])
		final[string]=val
	#print(final)
	#print(res)

	#print(sum(final['ILE5','TMPP303']))
	for key,val in res.items():
		for key2,val2 in final.items():
			if key[0] == key2[0] and key[2]==key2[1]:
				for i in range(len(val)):
					if res[key][i]==1:
						final[key2][i]=1
	
	def barcode(key_id):
		name=str(key_id[0])+'-'+str(key_id[1])
		
		with open(('%s.txt'% name),'w') as k:
			for i in range(len(final[key_id])):
				k.write('%s\n' % final[key_id][i][0])
		
		return

	#barcode(('ASP27','TMPP300'))
	#barcode(('ALA6','TMPP300'))
	#barcode(('THR113','TMPP300'))
	#barcode(('ILE5','TMPP300'))
	#barcode(('ARG28','TMPP300'))
	#barcode(('MET20','D4PP303'))
	#barcode(('ASP27','TMPP300'))


	summary={}

	#print(final)
	for i in final:
		count=0
		for j in range(len(final[i])):
			if final[i][j] ==1:
				count+=1
		pre_sum=count/size*100
		summary[i]=round(pre_sum,2)

	return summary

print(data_input(file,index_file))