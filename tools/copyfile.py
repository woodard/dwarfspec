# Copyright 2012 DWARF Debugging Information Format Committee
# This reads the input tokens and then
# writes them out in new files.  
# Used to verify that the output matches the input byte-for-byte

import sys
import fileio

def read_args():
  cur = 1
  filelist = []
  while  len(sys.argv) > cur:
    v = sys.argv[cur]
    filelist += [v]
    cur = int(cur) + 1

  dwf = fileio.readFilelist(filelist)

  dwf.dwwrite()

if __name__ == '__main__':
  read_args()
  


