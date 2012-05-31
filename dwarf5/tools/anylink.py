# Copyright 2012 DWARF Debugging Information Format Committee
#
# Handles the testing and update for all DW_* prefixes.
# Called by taglink and other convenience apps to do their work.
#
# Run as an app itself, the options are
#    python anylink [-t prefix] ... [-all] [file] ...
#    Use either -all or one or more -t, as in examples:
#    python anylink -t DW_ACCESS_ -t DW_OP_   test.in test2.in
#    python anylink -all    test.in test2.in 

import sys
import fileio

global mytarglist

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
  global mytarglist
  for mt  in mytarglist:
    if stdname.startswith(mt):
      if len(stdname) > len(mt):
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

def process_files(targlist,filelist):
  global mytarglist
  mytarglist = targlist
  dwf = fileio.readFilelist(filelist)
  dwf.dwtransformline(transfunc)
  dwf.dwwrite()

def read_file_args(targlist):
  cur = 1
  filelist = []
  while  len(sys.argv) > cur:
    v = sys.argv[cur]
    filelist += [v]
    cur = int(cur) + 1
  process_files(targlist,filelist)
  


legalprefix = ["DW_ACCESS_",
"DW_ADDR_",
"DW_AT_",
"DW_ATE_",
"DW_CC_",
"DW_CFA_",
"DW_CHILDREN_",
"DW_DSC_",
"DW_DS_",
"DW_END_",
"DW_FORM_",
"DW_ID_",
"DW_INL_",
"DW_LANG_",
"DW_LNE_",
"DW_LNS_",
"DW_MACINFO_",
"DW_OP_",
"DW_ORD_",
"DW_TAG_",
"DW_VIRTUALITY_",
"DW_VIS_" ]

def islegalprefix(prefix):
  for t in legalprefix:
    if t == prefix:
      # All is ok.
      return "y"
  return "n"

def printlegals():
  print >>sys.stderr,"legal targets  for -t options are: "
  for t in legalprefix:
    print >>sys.stderr, t
  

def read_all_args():
  filelist = []
  targlist = []
  cur = 1
  while  len(sys.argv) > cur:
    v = sys.argv[cur]
    if v == "-all":
      targlist = legalprefix
    elif v == "-t":
      cur = int(cur) + 1
      if cur >= len(sys.argv):
        print >> sys.stderr , "A -t has no target list entry"
        sys.exit(1)
      v2 = sys.argv[cur]
      if islegalprefix(v2) == "y":
        targlist += [v2]
      else:
        print >> sys.stderr , "A -t has invalid target list entry", v2
        printlegals()
        sys.exit(1)
    else:
      filelist += [v]
    cur = int(cur) + 1
  if len(targlist) < 1:
    print >> sys.stderr , "No targets specified."
    printlegals()
    sys.exit(1)
  if len(filelist) < 1:
    print >> sys.stderr , "No files specified."
    printlegals()
    sys.exit(1)
  process_files(targlist,filelist)

#  anylink [-t <class>] ... [file] ...

if __name__ == '__main__':
  read_all_args()

