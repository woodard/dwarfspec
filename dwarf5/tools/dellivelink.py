# Copyright 2013 DWARF Debugging Information Format Committee
# This reads the input tokens and then
# writes them out in new files.  

# October 5, 2013. 
# This replaces \livelink and \livetarg with 
# a simpler \DWXXXyyy, per Rob Brender email of Oct 4, 2013
# It strives to be idempotent, so rerunning makes no 
# further changes.

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


def append_to_out(out,addthese):
  for a in addthese:
    out += [a]


def doreplace(toks,curtoknum,lasttoknum):
  if int(curtoknum) + 6 > int(lasttoknum):
    return "n"
  if toks[curtoknum+1]._class != "ind" or ''.join(toks[curtoknum+1]._label) != "{":
    return "n"
  if toks[curtoknum+2]._class != "id":
    return "n"
  if toks[curtoknum+3]._class != "ind" or ''.join(toks[curtoknum+3]._label) != "}":
    return "n"
  if toks[curtoknum+4]._class != "ind" or ''.join(toks[curtoknum+4]._label) != "{":
    return "n"
  if toks[curtoknum+5]._class != "id":
    return "n"
  if toks[curtoknum+6]._class != "ind" or ''.join(toks[curtoknum+6]._label) != "}":
    return "n"
  return "y"

def newt(toks,curtoknum,finalchars,):
  s = ''.join(toks[curtoknum + 5]._label)
  s2 = "\\" + s + finalchars
  t = fileio.dwtoken()
  t.insertid(s2)
  return t

def transfunc(linetoks,myfile,linenum):
  if len(linetoks) < 1:
    return linetoks
  tnumin = 0
  changes = 0
  lasttoknum = len(linetoks) -1
  outtoks = []
  for x in linetoks:
    if tnumin > lasttoknum:
      break
    t = linetoks[tnumin]
    rawtok = ''.join(t._tex)
    if  rawtok == "\\newcommand" and tnumin == 0:
        # Do not touch newcommand stuff
        return linetoks
    if  rawtok == "\\livelink" and "y" == doreplace(linetoks,tnumin,lasttoknum):
        newtok = newt(linetoks,tnumin,"")
        outtoks += [newtok]
        tnumin += 7
        if int(tnumin)  <= int(lasttoknum):
          # not at end of line, Check to see if we want a {} or not.
          if linetoks[tnumin]._class == "ind" and  ''.join(linetoks[tnumin]._label) == " ":
            newtlb = fileio.dwtoken();
            newtlb.setIndivid("{")
            outtoks += [newtlb]
            newtrb = fileio.dwtoken();
            newtrb.setIndivid("}")
            outtoks +=  [newtrb]
    elif  rawtok == "\\livetarg" and "y" == doreplace(linetoks,tnumin,lasttoknum):
        newtok = newt(linetoks,tnumin,"TARG")
        outtoks += [newtok]
        tnumin += 7
        if int(tnumin) <= int(lasttoknum):
          # not at end of line. Check to see if we want a {} or not.
          if linetoks[tnumin]._class == "ind" and  ''.join(linetoks[tnumin]._label) == " ":
            newtlb = fileio.dwtoken();
            newtlb.setIndivid("{")
            outtoks += [newtlb]
            newtrb = fileio.dwtoken();
            newtrb.setIndivid("}")
            outtoks +=  [newtrb]
    else:
      tnumin = tnumin+ 1
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
  


