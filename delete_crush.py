import sys,os
import numpy as np

f_pdb=sys.argv[1]

i_wat=-1

f_name_list='crush.dat'
flist=open(f_name_list,'r')
name_list=[]
name_index=[]
for lines in flist:
  line=lines.split()
  if line[0]=='SPF':
    name_list.append(line[0])
    name_index.append(np.float(line[1]))
flist.close()

Nlist=len(name_index)
eps=1.0E-6

ff=open(f_pdb,'r')
for lines in ff:
  Nl=len(lines)
  if lines[0:4]=='ATOM':
    if lines[17:20]=='SPF':
      i_wat=i_wat+1
      if np.abs(name_index[i_wat]-1.0)<eps:
        #print lines[0:13]+"Na+ Na+ "+lines[21:Nl-1] ## For showing crushing waters.
        continue
      else:
        print lines[0:Nl-1]
    else:
      print lines[0:Nl-1]
  else:
    print lines[0:Nl-1]
ff.close()
