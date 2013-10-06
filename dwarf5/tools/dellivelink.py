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

insidealltt = "n"

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

def myjoinlabel(tok):
  s = ''.join(tok._label)
  return s

def doreplace(toks,curtoknum,lasttoknum):
  if int(curtoknum) + 6 > int(lasttoknum):
    return "n"
  if toks[curtoknum+1]._class != "ind" or myjoinlabel(toks[curtoknum+1]) != "{":
    return "n"
  if toks[curtoknum+2]._class != "id":
    return "n"
  if toks[curtoknum+3]._class != "ind" or myjoinlabel(toks[curtoknum+3]) != "}":
    return "n"
  if toks[curtoknum+4]._class != "ind" or myjoinlabel(toks[curtoknum+4]) != "{":
    return "n"
  if toks[curtoknum+5]._class != "id":
    return "n"
  if toks[curtoknum+6]._class != "ind" or myjoinlabel(toks[curtoknum+6]) != "}":
    return "n"
  return "y"


def newt(toks,curtoknum,finalchars,):
  s = myjoinlabel(toks[curtoknum + 5])
  s2 = "\\" + s + finalchars
  t = fileio.dwtoken()
  t.insertid(s2)
  return t

def checkalltt(linetoks,tnumin,lasttoknum,myfile,linenum):
    global insidealltt
    if int(tnumin) + 3 < int(lasttoknum):  
      return "n"
    t1 = linetoks[tnumin]
    s1 = myjoinlabel(t1)
    if  s1 != "\\begin" and s1 != "\\end":
      return "n"
    t2 = linetoks[tnumin+1]
    s2 = myjoinlabel(t2)
    if  s2 != "{":
      return "n"

    t3 = linetoks[tnumin+2]
    s3 = myjoinlabel(t3)
    if  s3 != "alltt":
      return "n"

    t4 = linetoks[tnumin+3]
    s2 = myjoinlabel(t4)
    if  s2 != "}":
      return "n"

    if  s1 == "\\begin":
      if insidealltt =="y":
        print "nested \\begin{alltt} is an error in",myfile._name, " at ",linenum
      insidealltt = "y" 
    if  s1 == "\\end":
      if insidealltt =="n":
        print "nested \\end{alltt} is an error in",myfile._name, " at ",linenum
      insidealltt = "n" 

def transfunc(linetoks,myfile,linenum):
  global insidealltt
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
    checkalltt(linetoks,tnumin,lasttoknum,myfile,linenum)
    if  rawtok == "\\livelink" and "y" == doreplace(linetoks,tnumin,lasttoknum):
        newtok = newt(linetoks,tnumin,"")
        outtoks += [newtok]
        tnumin += 7
        if int(tnumin)  <= int(lasttoknum):
          # not at end of line, Check to see if we want a {} or not.
          if  insidealltt == "n" and linetoks[tnumin]._class == "ind" and  myjoinlabel(linetoks[tnumin]) == " ":
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
          if insidealltt == "n" and linetoks[tnumin]._class == "ind" and  myjoinlabel(linetoks[tnumin]) == " ":
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
  


