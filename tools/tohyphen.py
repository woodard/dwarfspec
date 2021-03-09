# Copyright 2012 DWARF Debugging Information Format Committee
#
# Convert DW_ and DW\_ names to DW\-\_ 
# python tohyphen.py *.tex
# The output files have .out appended to the name.

import sys
import fileio

def convertToHyphen(s):
  out = []
  for c in s:
    if c == "_":
      out += ["\\"]
      out += ["-"]
      out += ["\\"]
    out += [c]  
  os = ''.join(out)
  return os

def transfunc(linetoks,myfile,linenum):
  if len(linetoks) < 1:
    return linetoks
  outtoks = []
  for t in linetoks:
    stdname= ''.join(t._std)
    if stdname.startswith("DW_") != 0:
      xs = convertToHyphen(stdname)
      x = fileio.dwtoken()
      x.insertid(xs)
      x.finishUpId()
      outtoks += [x]
    else:
      outtoks += [t]
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
  dwf.dwwrite()

if __name__ == '__main__':
  read_args()
  


