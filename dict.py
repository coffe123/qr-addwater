import os,sys
### This script for transforming the Gromacs names into AMBER names.
### If one wants to do the reverse, please change it accordingly.
### Yongle Li, Aug 23, 2016


fname=sys.argv[1]
ff=open(fname,'r')
rname='   '
aname='    '
for lines in ff:
  Nlines=len(lines)
  if Nlines>1:
    line=lines.split()
    rname=line[3]
    aname=line[2]
    k=0
    #print aname
    if aname=='HB1' and rname!='ALA':
       aname='HB2'
       k=1
       #print "HB1 -> ", aname
    if aname=='HB2' and k==0 and rname!='ALA':
       aname='HB3'
    if aname=='HG1' and rname!='THR':
       aname='HG2'
       k=1
    if aname=='HG2' and k==0:
       aname='HG3'
    if aname=='HA1':
       aname='HA2'
       k=int(line[1])
    if aname=='HA2' and k<int(line[1]):
       aname='HA3'
    if aname=='1HG1' and rname=='ILE':
       aname='HG12'
    if aname=='2HG1' and rname=='ILE':
       aname='HG13'
    if aname=='HD1' and rname=='ILE':
       aname='HD11'
    if aname=='HD2' and rname=='ILE':
       aname='HD12'
    if aname=='HD3' and rname=='ILE':
       aname='HD13'
    if aname=='CD'  and rname=='ILE':
       aname='CD1'
    if aname=='HD1' and rname=='LYS':
       aname='HD2'
       k=int(line[1])
    if aname=='HD2' and rname=='LYS' and k<int(line[1]):
       aname='HD3'
    if aname=='HE1' and rname=='LYS':
       aname='HE2'
       k=int(line[1])
    if aname=='HE2' and rname=='LYS' and k<int(line[1]):
       aname='HE3'
    if aname=='HD1' and rname=='ARG':
       aname='HD2'
       k=1
    if aname=='HD2' and rname=='ARG' and k==0:
       aname='HD3'
    if aname=='HD1' and rname=='PRO':
       aname='HD2'
       k=1
    if aname=='HD2' and rname=='PRO' and k==0:
       aname='HD3'
    ##lines[12:16]=aname
    if aname=='OC1':
       aname='O'
    if aname=='OC2':
       aname='OXT'
    if aname=='1HE2' and rname=='GLN':
       aname='HE21'
    if aname=='2HE2' and rname=='GLN':
       aname='HE22'

    if len(aname)<3:
      lines=lines[0:12]+'{:^4s}'.format(aname)+lines[16:-1]
    else:
      lines=lines[0:12]+'{:>4s}'.format(aname)+lines[16:-1]
  print lines
  k=0
