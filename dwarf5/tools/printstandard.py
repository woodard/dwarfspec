# Copyright 2012 DWARF Debugging Information Format Committee
#
# Print the DW_* entries (and only them) one per line,
# with no \_ or \-.
# Try    
#           python printstandard.py *.tex  |sort|uniq

# Useful in case certain random typos creep in to the .tex

import sys
import fileio

def transfunc(linetoks,myfile,linenum):
  if len(linetoks) < 1:
    return linetoks
  tnumin = 0
  changes = 0
  lasttoknum = len(linetoks) -1
  outtoks = []
  for t in linetoks:
    stdname= ''.join(t._std)
    if stdname.startswith("DW_") != 0:
        print stdname
    # End of for loop.
  return outtoks

def read_args():
  cur = 1
  filelist = []
  while  len(sys.argv) > cur:
    v = sys.argv[cur]
    filelist += [v]
    cur = int(cur) + 1

  dwf = fileio.readFilelist(filelist)
  dwf.dwtransformline(transfunc)

if __name__ == '__main__':
  read_args()
  


