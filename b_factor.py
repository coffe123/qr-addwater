### Script by Pavel, modified by Yongle.

from __future__ import division
import sys,os
import iotbx.pdb
import time
import mmtbx.f_model
from iotbx import reflection_file_reader

def compute(f_name):
  miller_arrays = reflection_file_reader.any_reflection_file(file_name =
    f_name+'.mtz').as_miller_arrays()
  for ma in miller_arrays:
    print ma.info().label_string()
    if(ma.info().label_string()=="IOBS,SIGIOBS"):
      f_obs = ma
    if(ma.info().label_string()=="R-free-flags"):
      r_free_flags = ma
  f_obs, r_free_flags = f_obs.common_sets(r_free_flags)
  r_free_flags = r_free_flags.array(data = r_free_flags.data()==0)
  #
  pdb_inp = iotbx.pdb.input(file_name=f_name+".pdb")
  xray_structure = pdb_inp.xray_structure_simple()
  #
  fmodel = mmtbx.f_model.manager(
    f_obs          = f_obs,
    r_free_flags   = r_free_flags,
    xray_structure = xray_structure)
  fmodel.update_all_scales()
  print "r_work=%6.4f r_free=%6.4f"%(fmodel.r_work(), fmodel.r_free())
  fmodel.show(show_header=False, show_approx=False)

if (__name__ == "__main__"):
  t0 = time.time()
  f_name=sys.argv[1]
  compute(f_name)
  print "Total time: %-8.4f"%(time.time()-t0)
  print "OK"

