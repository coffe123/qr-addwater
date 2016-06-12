# qr-addwater

TODO: Since the RISM is updated in Apr. 2016, the new version of it is under testing. 

Scripts for adding water using 3D-RISM, and modeling for MD simulation.
Before use, please double check the AMBER14+ is installed, and the $AMBERHOME is setted.
Also, three sets of self-developed parameters are available: 

1.  EDO

2.  NO3-

3.  ACT-


To use:

1. Please find the force field parameters in the directory: $AMBERHOME/dat/rism1d/model/
If there is no parameter you want, you must use standard RESP method to fit partial charge, 
and then use GAFF to create the .prep/.lib file and corresponding .frcmod file, 
and then create the force field parameter file in that directory.


2. One may need to specify the density of the small molecules to add.


3. After adding water molecules, one can use b_factor.py to compute B-factor with corresponding mtz file.
This file can be obtained by using phenix.fetch_pdb.
It may be better to do a preliminary optimization before comparing the B-factor.

4. Please note, the speed of RISM calculation is O(N^3), 
so if one needs to add lots of different species, the better way is to do this severial times, 
and take the added molecules as part of the protein before doing following adding. 

5. After adding waters using 3D-RISM, please use get_farwater.py, delete_farwater.py, get_crush.py, and delete_crush.py to delete redundant waters. The redundant water molecules can come from two ways: 1st, the 3D-RISM I used does not deal with periodical boundary condition, so the far water molecules may not proper in the crystal environment. 2nd, after PBC added, some water molecules will get too close to the image molecules (image protein, image solvent, etc.). So it's better to delete both of the two types of water molecules. The current used parameters are:

a. r_cut_far=3.70
b. r_cut_crush=2.80

The parameters are used for obtain proper volume during MD simulation. The finding of far water is arbitary, but the 2.80 is the sum of the radius of water molecule. Both of the cut off radius should be test extensively to give proper volume. The criteria of volume is within 0.3% relative error during MD. 

6. After delete the redundant water molecules, one needs to use XtalSetup.sh to add some additional water molecules again, to fill out the vacuum bubbles in the prime cell. The number of water molecules can be adjusted in the parameter of AddToBox in AMBER suit. This parameter is also need to extensive test.

################################################################

Known bug: In the line 13 of b_factor.py, the mtz file may not contain characters "IOBS,SIGIOBS" but other ones. 
Please change the content correspondingly.
