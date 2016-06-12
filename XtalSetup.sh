#!/bin/bash
# This script illustrates the protocol for setting up a simulation of a protein
# crystal unit cell.  Source codes for all programs called by this tutorial are
# present in this directory; the script will check for the existence of any
# programs that it needs and prompt the user to compile them if necessary.
#
# All programs in this tutorial may be run independently, and will produce lists
# of options if run with no arguments.  All programs needed for this tutorial
# can be run from the command line; no separate input files are needed.

# In order to run this tutorial, paths to certain AMBER programs must be set:
TLEAP="/home/Yongle/Research/sources/amber16/bin/tleap"

# PART 1

# PART 2
# PART 3

# These variables define the unit cell dimensions, and correspond to the CRYST1
# record of the original PDB file, 2vb2.pdb.
###CRYST1   27.070   31.250   33.760  87.98 108.00 112.11 P 1           1          
CDX="27.070"
CDY="31.250"
CDZ="33.760"
ALPHA="87.98"
BETA="108.00"
GAMMA="112.11"
XYZ="-X ${CDX} -Y ${CDY} -Z ${CDZ}"
ABC="-al ${ALPHA} -bt ${BETA} -gm ${GAMMA}"

# This is the first AddToBox command, for adding acetate.

## This is the third and final AddToBox command, for adding water.
  ${AMBERHOME}/bin/AddToBox \
    -c 2vb2.filtered.pdb \
    -a spce.pdb \
    -na  15 \
    -o solv2vb2.pdb \
    -P 1415 \
    -RP 3.0 \
    -RW 3.0 \
    -G 0.1 \
    -V 1 \
    ${XYZ} \
    ${ABC}

sed 's/SPF/WAT/' solv2vb2.pdb > solv2vb2.b.pdb

cat > solvate.tleap << EOF
source leaprc.ff99SB_spce
source leaprc.gaff2
loadAmberPrep Acetate.prp
loadAmberPrep Ammonium.prp
loadamberprep NO3.prepc
loadamberprep EDO.prepc
ammparms = loadAmberParams Ammonium.frcmod
loadamberparams frcmod.ions1lm_126_spce
loadamberparams NO3.frcmod
loadamberparams EDO.frcmod

x = loadPdb "solv2vb2.b.pdb"
bond x.6.SG x.127.SG
bond x.30.SG x.115.SG
bond x.64.SG x.80.SG
bond x.76.SG x.94.SG
setBox x vdw 1.0
check x
addions2 x Na+ 0
saveAmberParm x solv2vb2.top solv2vb2.crd
quit
EOF

# Run the TLEAP program to create the starting coordinates and topology
${TLEAP} -s -f solvate.tleap

## Run ChBox to edit the last line of the initial coordinates file so that it
## matches the true unit cell dimensions specified in 2vb2.pdb.
mv solv2vb2.crd tmp
${AMBERHOME}/bin/ChBox -c tmp -o solv2vb2.crd ${XYZ} ${ABC}
mv solv2vb2.crd solv2vb2.inpcrd
mv solv2vb2.top solv2vb2.prmtop
