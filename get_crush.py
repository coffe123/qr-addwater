import numpy as np
import sys
#a=[[]]*2
#res=[]
#res_coord=[]
#res_name=[]
#f1=sys.argv[1]
#TOM     13  CE ALYS A   1      -1.966   8.606  10.745  0.69  5.10           C

  ### First cycle, to recognize all the number and names for the residues.
def read_res(f1):
  print "read: ",f1
  res=[]
  res_coord=[]
  res_name=[]
  ff=open(f1,'r')
  i_res=1
  i=0
  j=0
  for lines in ff:
    #if lines[0:6]=='CRYST1':
    #  A=float(lines[6:15])
    #  B=float(lines[15:24])
    #  C=float(lines[24:33])
    #  alpha=float(lines[33:40])
    #  beta =float(lines[40:47])
    #  gamma=float(lines[48:54])
    if lines[0:4]=='ATOM' or lines[0:6]=='HETATM':
      i=i+1
      if i==1: ## The first residue always exists.
         ## This is for j==0 case.
         res.append([])
         res_coord.append([])
         res_name.append(lines[17:20])
      temp_res=int(lines[22:26])
      if temp_res!=i_res:
        #  print "The old res number and the new one are different."
        #  print temp_res, i_res
        j=j+1
        #  print "The"+'{:8g}'.format(j)+" residue."
        #  print "===="
        res.append([])
        res_coord.append([])
        res_name.append(lines[17:20])
        i_res=temp_res
  ff.close()
  Nj=j+1
  return res, res_coord, res_name,Nj

  ### 2nd time for opening.
  ### For read information for atoms in each residue.
def read_atm_coord(f1,res,res_coord,Nj):
  print "read 2: ", f1
  ff=open(f1,'r')
  i=-1
  j=0
  for lines in ff:
    if lines[0:4]=='ATOM' or lines[0:6]=='HETATM':
      i=i+1
      if i==0:
        i_res=int(lines[22:26])
      temp_res=int(lines[22:26])
      if temp_res!=i_res:
        j=j+1
        if j<Nj:
          #print j, res[j], res_name[j]
          res[j].append(lines[12:16])
          res_coord[j].append([float(lines[30:38]),\
                               float(lines[38:46]),\
                               float(lines[46:54])])
          #print '{:8d}'.format(j-1)+" residue information:"
          #print res[j-1]
          #print res_coord[j-1]
          #print "========"
        i_res=temp_res
      else:
        res[j].append(lines[12:16])
        res_coord[j].append([float(lines[30:38]),\
                             float(lines[38:46]),\
                             float(lines[46:54])])
  ff.close()
  return res, res_coord

### This part is for checking the read-in residues.
# for i in range(Nj):
#   print "Here is residue: ", res_name[i]
#   print "The atom list: "
#   res_atmnum=len(res[i])
#   for j in range(res_atmnum):
#     print res[i][j], res_coord[i][j][0],res_coord[i][j][1],res_coord[i][j][2]
# 
#   print "======================="

ref_pdb=sys.argv[1]

print "We will do: "
print ref_pdb
print "============"
ref_res_temp,ref_res_coord_temp,ref_res_name,N_ref = \
   read_res(ref_pdb)
ref_res_temp,ref_res_coord_temp                    = \
   read_atm_coord(ref_pdb,ref_res_temp,ref_res_coord_temp,N_ref)
ref_res      =ref_res_temp[:]
ref_res_coord=ref_res_coord_temp[:]
print "Finished reading."

## This is a check for memory usage of the arrays.
## print id(ref_res_coord_temp)
## print id(ref_res_coord)
## print ref_res_coord
## print ref_res_coord[0][0][0],  ref_res_coord[0][0][1],  ref_res_coord[0][0][2]
ref_label=np.zeros(len(ref_res))
print "===="
dist_crit=2.80 ### The criterion for definition of 'crush.'

other_pdb_list=sys.argv[2]
f_list=open(other_pdb_list,'r')
ll=0
for tmp_cmpr_pdb in f_list:
  Ncmpr_pdb=len(tmp_cmpr_pdb)
  cmpr_pdb=tmp_cmpr_pdb[0:Ncmpr_pdb-1] 
  # if ll==1:
  print ref_pdb, cmpr_pdb
  cmpr_res,cmpr_res_coord,cmpr_res_name,N_cmpr=read_res(cmpr_pdb)
  cmpr_res,cmpr_res_coord=read_atm_coord(cmpr_pdb,cmpr_res,cmpr_res_coord,N_cmpr)
  #print "ref0:  ",ref_res_coord[0][0][0],  ref_res_coord[0][0][1],  ref_res_coord[0][0][2]
  #print "cmpr0: ",cmpr_res_coord[0][0][0], cmpr_res_coord[0][0][1], cmpr_res_coord[0][0][2]
  for i in range(N_ref):
    Ni=len(ref_res_coord[i])
    for l in range(Ni):
      for j in range(N_cmpr):
        Nj=len(cmpr_res_coord[j])
        for k in range(Nj):
          dist=0.0
          for mm in range(3):
            dist=dist+(ref_res_coord[i][l][mm]-cmpr_res_coord[j][k][mm])**2
          dist=np.sqrt(dist)
          if dist<dist_crit:
##            print "%4d %4d %4s %4s %8.3g" % [i, j, ref_res_name[i],cmpr_res_name[j], dist]
             # print i, j, ref_res_name[i],cmpr_res_name[j], dist, cmpr_pdb
             ref_label[i]=1
  # break  
  print "========END========="+cmpr_pdb
  #break
  ll=ll+1

for i in range(N_ref):
  print ref_res_name[i], ref_label[i]
