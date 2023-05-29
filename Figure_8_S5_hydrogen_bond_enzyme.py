from collections import defaultdict
from collections import OrderedDict
import matplotlib.pyplot as plt 
import itertools
import numpy as np

file='tmpp-l28r-5'

def merging_bonds(file):
    index={}
    #index list from VMD 1207 -- DHF161 NH 1130 -- ARG28 NE 
    with open(str(file)+'-index.dat') as f:
        for line in f:
            line=line.split(' ')
            index[line[0]]=[line[1],line[2][0:-1]]


    trj=defaultdict(list)

    counter=0
    b=()
    with open(str(file)+'-hbond.dat') as g:
        for line in g:
            a=line.split(' ')
            #print(a)
            if a[0]=='freeSelLabel':
                continue
            elif a[0][0:-1]=="#":
                continue
            elif a[0]=="#":
                continue
            elif a[0] =='freeSelString':
                b=(a[3],a[4])
                trj[b]=list()
            elif line==None:
                break
            elif line:
                trj[b].append([a[0],a[1][0:-1]])
                counter+=1

    for key,val in trj.items():
        length =len(trj[key])

    occ=[]*length
    pro={}
    #print(len(trj))
    for key,val in trj.items():
    #print(val)
        for line in val:
            occ.append(float(line[1]))
    #print(frame)
    #print(occ)   #print(i)
        pro[key]=occ
        occ=[]
 

    final=OrderedDict(sorted(pro.items(),key=lambda x:x[0]))
    
    res=defaultdict(list)
    
    for key,val in final.items():
        if key[0] in index.keys():
            new_key_don = index.get(key[0])
            new_key_don = tuple(new_key_don)
            new_key_acc = index.get(key[1][0:-1])
            #print(type(new_key_acc))
            new_key_acc=tuple(new_key_acc)
            #print(type(new))
            new_key=new_key_don+new_key_acc
            val1=final.get((key[0],key[1]))
            res[new_key].append(val1)
    
    
    
    res_pair = defaultdict(list)
    for key,val in res.items():
        #print(key)
        res_pair[key[0],key[2]].append(val)
    
    
    #print(res_pair['ASP27','DHF161'])
    #for key,val in res_pair.items():
    #	print(key,val,'\n')

    #occ_dict=defaultdict(lambda: [0]*length)
    
    

    occ_dict={}

    for x,y in res_pair.items():
    	list1=[]
    	for a in y:
    		list1.append(a[0])
    	occ_dict[x]=list1
    
    bos={}
    for x in occ_dict:
    	bos[x]=[0]*length



    for x in bos:
        for a in occ_dict:
            if x==a:
                for m1 in range(len(occ_dict[a])):
                    list1=occ_dict[a][m1]
                    for m2 in range(len(list1)):
                        if bos[x][m2]==0 and list1[m2]==1:  
                            bos[x][m2]=1
                        
                            
    #print(bos['ASP69','ARG71'])
     
    final_dict={}
    
    for i in bos:
        count=0
        for j in range(len(bos[i])):
            if bos[i][j] ==1:
               count+=1
        pre_sum=count/length*100
        final_dict[i]=round(pre_sum,2)

    """total=0
    for key,val in bos.items():

        for ley in val:
            #print(ley)
            total += ley
        #print(sum)
        pre_sum=total/length*100
        final_dict[key]=round(pre_sum,2)
        #print(pre_sum)
        total=0"""

    #print(final_dict['DHF161','ARG57'])
    
    #print(final_dict['SER150','ASP116'])
        
    print(len(final_dict))
    return(final_dict)

def wt_occ(wt1,wt2,wt3,wt4,wt5,weight):

    wtc={k: wt1.get(k, 0) + wt2.get(k, 0) + wt3.get(k,0) + wt4.get(k,0) + wt5.get(k,0) for k in set(wt1) | set(wt2) | set(wt3) | set(wt4) | set(wt5)}

    wtc = {k: v / weight for k, v in wtc.items()}		
    return wtc



def occ_diff(mutant,wtc):
    difference={}

    for hbond1 in mutant:
        for hbond2 in wtc:
            a=[]
            if hbond1==hbond2:
                val1=mutant.get(hbond1)
                val2=wtc.get(hbond2)
                difference[hbond1]=[float(val1),float(val2),round(float(val1)-float(val2),2)]
    add_list={}

    #add wtc hbonds not present in mutant
    for d in wtc:
        if d not in mutant:
            val1=wtc.get(d)
            z=round(val1,2)
            add_list[d]=[0,z,-z]

    #add mutant hbonds not present in wtc
    for s in mutant:
        if s not in wtc:
            val3=mutant.get(s)
            y=round(val3,2)
            add_list[s]=[y,0,y]

    difference.update(add_list)

    top_bonds={}

    for key in difference:
        for item in [difference[key][len(difference[key])-1]]:
            if abs(item) >= 0 :
                val=difference.get(key)
                if key in top_bonds:
                    top_bonds.append(key)
                else:
                    top_bonds[key]=val
    dhf={}
    for key,value in difference.items():
        if 'DHF'in key[0] or 'DHF' in key[1]:
            #print('bugn Salimin doum gunu')
            dhf[key]=value
    
    m_file=str(file)+"-dhf-bonds.txt"

    with open(m_file,'w') as f:
        for key, value in dhf.items():
            f.write('%s-%s :  %s %s %s\n' % (key[0],key[1], value[0],value[1],value[2]))

    return top_bonds


mutant=merging_bonds(file)
wt1=merging_bonds('tmpp-wt-1')
wt2=merging_bonds('tmpp-wt-2')
wt3=merging_bonds('tmpp-wt-3')
wt4=merging_bonds('tmpp-wt-4')
wt5=merging_bonds('tmpp-wt-5')

wt=wt_occ(wt1,wt2,wt3,wt4,wt5,5)

wt_compared=occ_diff(mutant,wt)



def merged_bonds_write(file):
    m_file=str(file)+"-merged-bonds.txt"

    with open(m_file,'w') as f:
        for key, value in mutant.items():
            f.write('%s-%s :  %s\n' % (key[0],key[1], value))

    w_file='wt'+'-merged-bonds'

    with open('{}.txt'.format(str(w_file)),'w') as k:
        for bond, percent in wt.items():
            k.write('%s-%s :  %s\n' % (bond[0],bond[1], percent))

    diff_file=str(file)+'-wtc-0%-bonds.dat'

    with open(diff_file,'w') as g:
        for key,val in wt_compared.items():
            g.write('%s-%s:    %s %s %s\n' % (key[0],key[1], val[0],val[1],val[-1]))

merged_bonds_write(file)