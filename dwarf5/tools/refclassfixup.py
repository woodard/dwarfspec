# Copyright 2012 DWARF Debugging Information Format Committee
# This reads the input tokens and then
# writes them out in new files.  
# Used to verify that the output matches the input byte-for-byte

import sys
import fileio

refclass = { 
#"address":"chap:address", 
#"block":"chap:block", 
#"constant":"chap:constant", 
"exprloc":"chap:exprloc", 
#"flag":"chap:flag",
"lineptr":"chap:lineptr",
"loclistptr":"chap:loclistptr",
"macptr":"chap:macptr",
"rangelistptr":"chap:rangelistptr" }
#"reference":"chap:reference",
#"string":"chap:string" }

def ischar(tok,c):
   if tok._class != "ind":
      return "n"
   if len(tok._tex) != 1:
       return "n"
   if tok._tex[0] != c:
       return "n"
   return "y"

def transformone(tok, string):
  label = refclass[string]
  # output is  \livelink{label}{string}
  t1=fileio.dwtoken()
  t1.insertid("\livelink")
  t2=fileio.dwtoken()
  t2.setIndivid("{")
  t3=fileio.dwtoken()
  t3.insertid(label)
  t4=fileio.dwtoken()
  t4.setIndivid("}")
  t5 = t2
  t6=fileio.dwtoken()
  t6.insertid(string) 
  t7 = t4
  return [t1,t2,t3,t4,t5,t6,t7]

def append_to_out(out,addthese):
  for a in addthese:
    out += [a]

def transfunc(linetoks):
  if len(linetoks) < 1:
    return linetoks
  tnumin = 0
  changes = 0
  lasttoknum = len(linetoks) -1
  outtoks = []
  for t in linetoks:
    rawtok = ''.join(t._tex)
    if  refclass.has_key(rawtok) == 1:
      if tnumin == 0 or tnumin == lasttoknum:
         tmp = transformone(t, rawtok);
         changes = changes +  1
         append_to_out(outtoks,tmp)
      else:
        if  ischar(linetoks[tnumin - 1],"{") == "n" and ischar(linetoks[tnumin+1],"}") == "n":
          tmp = transformone(t, rawtok);
          append_to_out(outtoks,tmp)
          changes = changes +  1
        else:
          outtoks += [t]
    else:
      outtoks += [t]
    tnumin = tnumin+ 1
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
  


