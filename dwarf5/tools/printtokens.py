# Copyright 2012 DWARF Debugging Information Format Committee
# This simply prints the input tokens.
# Used to verify basic sanity of the reading code.

import sys
import fileio

def print_args():
  cur = 1
  filelist = []
  while  len(sys.argv) > cur:
    print "argv[",cur,"] = ", sys.argv[cur]
    v = sys.argv[cur]
    filelist += [v]
    cur = int(cur) + 1

  dwf = fileio.readFilelist(filelist)
  dwf.dwprint()

if __name__ == '__main__':
  print_args()
  


