# Copyright 2012 DWARF Debugging Information Format Committee
#
# All DW_TAG_* entries not in {} are turned into \livelink.

import sys
import fileio

def ischar(tok,c):
   if tok._class != "ind":
      return "n"
   if len(tok._tex) != 1:
       return "n"
   if tok._tex[0] != c:
       return "n"
   return "y"

def transformone(tok,stdname,labelname):

  # output is  \livelink{label}{string}
  t1=fileio.dwtoken()
  t1.insertid("\livelink")
  t2=fileio.dwtoken()
  t2.setIndivid("{")
  t3=fileio.dwtoken()
  t3.insertid(labelname)
  t4=fileio.dwtoken()
  t4.setIndivid("}")
  t5 = t2
  t6=fileio.dwtoken()
  t6.insertid(''.join(tok._tex)) 
  t7 = t4
  return [t1,t2,t3,t4,t5,t6,t7]

def append_to_out(out,addthese):
  for a in addthese:
    out += [a]

def isdesiredname(stdname):
  """ If it is DW_TAG_* we return "y".
      Else return "n"
      We don't want something like plain DW_TAG  or 
      plain DW_TAG_ to get modified.
  """
  if stdname.startswith("DW_TAG_"):
    if len(stdname) > 7:
      return "y"
  return "n"

def dwspace(tok):
  if ischar(tok," ") == "y":
    return "y"
  if ischar(tok,"\t") == "y":
    return "y"
  return "n"
  
# Here we are a bit careful, in that accidental spaces
# after { or before } should not be confused with
# not having a {} around a name.
def leaderislbrace(linetoks,num):
  cnum = num - 1
  while cnum >= 1:
    tok = linetoks[cnum]
    if dwspace(tok) == "y":
      cnum = cnum - 1
      continue
    if ischar(tok,"{") == "y":
      return "y"
    return "n"
  return "n"
  
def trailerisrbrace(linetoks,num):
  cnum = num + 1
  while cnum < len(linetoks) :
    tok = linetoks[cnum]
    if dwspace(tok) == "y":
      cnum = cnum + 1
      continue
    if ischar(tok,"}") == "y":
      return "y"
    return "n"
  return "n"

def transfunc(linetoks):
  if len(linetoks) < 1:
    return linetoks
  tnumin = 0
  changes = 0
  lasttoknum = len(linetoks) -1
  outtoks = []
  for t in linetoks:
    rawtok = ''.join(t._tex)
    stdname= ''.join(t._std)
    linkname = "chap:" + ''.join(t._label)
    if isdesiredname(stdname) == "y":
      #Look past spaces when looking for { or }
      if leaderislbrace(linetoks,tnumin) == "n" or trailerisrbrace(linetoks,tnumin) == "n":
        tmp = transformone(t,stdname,linkname);
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
  


