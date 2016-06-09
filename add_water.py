import sys,os

### Stage 1 in Step 0: Adding H using reduce. 
### Todo: Change to other adding H program.
pdb_header=sys.argv[1]
Nh=len(pdb_header)
if Nh>4:
  pdb_header=pdb_header[0:4]

cmd="reduce --NOFLIP "+pdb_header+".pdb > "+pdb_header+".addH.pdb"
os.system(cmd)

### Stage 2 in Step 0: Prepare the prmtop file.
f1="tleap.in"
ff=open(f1,'w')

ff.write("source leaprc.ff14SB\n")
ff.write("source gaff\n")
ff.write("m = loadpdb "+pdb_header+".addH.pdb\n")
ff.write("saveamberparm m "+pdb_header+".prmtop "+pdb_header+".inpcrd\n")
ff.write("savepdb m "+pdb_header+".leap.pdb\n")
ff.write("quit\n")
ff.close()
cmd="tleap -s -f tleap.in"
os.system(cmd)
cmd="rm tleap.in"
os.system(cmd)

### Step 1: 1D-RISM
cmd="echo $AMBERHOME"
import commands
status, AMBERHOME = commands.getstatusoutput(cmd)
filename_rism1d="TP3_NaCl"
f1=filename_rism1d+".inp"
ff=open(f1,'w')
ff.write("&PARAMETERS\n")
ff.write("OUTLST='x', THEORY='DRISM', CLOSUR='KH',\n")
ff.write("!grid\n")
#ff.write("NR=16384, DR=0.025, routup=384, toutup=0,\n")
ff.write("NR=16384, DR=0.025, rout=0, kout=0, \n") ## Parameters of grid.
ff.write("!MDIIS\n")
#ff.write("NIS=20, DELVV=0.3, TOLVV=1.e-12,\n")
ff.write("mdiis_nvec=20, mdiis_del=0.3, tolerance=1.e-12,\n")
ff.write("maxstep=10000,\n")
ff.write("!iter\n")
ff.write("KSAVE=-1, KSHOW=1, maxste=10000,\n")
ff.write("!ElStat\n")
ff.write("SMEAR=1, ADBCOR=0.5,\n")
ff.write("!bulk solvent properties\n")
ff.write("TEMPERATURE=298, DIEps=78.497,\n") ### Temperature and epsilon of solvent.
ff.write("NSP=3\n") ## Number of species.
ff.write("/\n")
ff.write("&SPECIES\n")
ff.write("DENSITY=55.5d0,\n")
ff.write("MODEL=\""+AMBERHOME+"/dat/rism1d/model/TP3.mdl\"\n")
ff.write("/\n")
ff.write("&SPECIES\n")
ff.write("DENSITY=0.005d0,\n")
ff.write("MODEL=\""+AMBERHOME+"/dat/rism1d/model/Na+.mdl\"\n")
ff.write("/\n")
ff.write("&SPECIES\n")
ff.write("DENSITY=0.005d0,\n")
ff.write("MODEL=\""+AMBERHOME+"/dat/rism1d/model/Cl-.mdl\"\n")
ff.write("/\n")
ff.close()
cmd="rism1d "+filename_rism1d+" > "+filename_rism1d+".out || goto error"
os.system(cmd)

## Step 2: 3D-RISM
cmd="rism3d.snglpnt --pdb "+pdb_header+".addH.pdb \
    --prmtop "+pdb_header+".prmtop \
    --closure kh --guv "+pdb_header+" --xvv "+filename_rism1d+".xvv"
os.system(cmd)

cmd="placevent.py "+pdb_header+".O.1.dx 55.5 > O.pdb"
os.system(cmd)

### Remove all the temporary files.
cmd="rm *.dx"
os.system(cmd)
cmd="rm "+filename_rism1d+".*"
os.system(cmd)
###

cmd="awk '$1!~/^#/ && $1!~/^$/ {print}' O.pdb | m4 -DBCD=HOH | m4 -DD=O > WAT.pdb"
os.system(cmd)

cmd="cat "+pdb_header+".pdb WAT.pdb > "+pdb_header+".placevent.pdb"
os.system(cmd)
