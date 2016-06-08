# qr-addwater

Scripts for adding water using 3D-RISM, and modeling for MD simulation.
Before use, please double check the AMBER14+ is installed, and the $AMBERHOME is setted.

To use:
1. Please find the force field parameters in the directory: $AMBERHOME/dat/rism1d/model/
If there is no parameter you want, you must use standard RESP method to fit partial charge, 
and then use GAFF to create the .prep/.lib file and corresponding .frcmod file, 
and then create the force field parameter file in that directory.

2. One may need to specify the density of the small molecules to add.

3. After adding water molecules, one can use b_factor.py to compute B-factor with corresponding mtz file.
This file can be obtained by using phenix.fetch_pdb.
It may be better to do a preliminary optimization before comparing the B-factor.
Known bug: In the line 13, the mtz file may not contain characters "IOBS,SIGIOBS" but other ones. 
Please change the content correspondingly.
