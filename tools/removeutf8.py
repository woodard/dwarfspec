# Copyright 2012 DWARF Debugging Information Format Committee
#
# 
# 
# Looks for certain multi-byte chars and replaces with
# appropriate ascii.
# See "The Comprehensive LaTeX Symbol List"
#http://www.tex.ac.uk/tex-archive/info/symbols/comprehensive/symbols-a4.pdf

#\newcommand{\singlequote}[1]{\textquitedblleft#1\textquotedblright}
#\newcommand{\doublequote}[1]{\textquoteleft#1\textquoteright}

#
#  utf         latex                 description
# e2 80 9c      \textquotedblleft    (two curly left quote chars)  
# e2 80 9d      \textquotedblright   (two curly right quote chars)
#              or \doublequote{stringtoquote} (our command)
# e2 80 99      \textquoteleft       (single curly left quote char)
# e2 80 9b      \textquoteright      (single curly right quote quote char)
#      by itself for contractions like don't
#      or \singlequote{stringtoquote} for a left right pair (our command)
#
# e2 80 93       \textendash         (minus sign)
# e2 80 94      \textemdash          (long dash         )
#        \textthreequartersemdash (long dash, from textcomp package)
#               \textendash          (long dash         )
#               \leftrightline (from MnSymbol package)
# e2 80 a6     \dots         (...)
#                 \textellipsis  is also usable.
# e2 84 a2      \texttrademark      trademark symbol
# e2 ?? ??      \copyright          (copyright symbol)

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

def isutf80prefix(t):
  if t[0] != chr(226):
    return "n"
  if t[1] != chr(128):
    return "n"
  return "y"
def isutf84prefix(t):
  if t[0] != chr(226):
    return "n"
  if t[1] != chr(132):
    return "n"
  return "y"

def isutfleftdouble(t):
  if isutf80prefix(t) != "y":
    return "n"
  if t[2] != chr(156):
    return "n"
  return "y"
def isutfrightdouble(t):
  if isutf80prefix(t) != "y":
    return "n"
  if t[2] != chr(157):
    return "n"
  return "y"
def isutfleftsingle(t):
  if isutf80prefix(t) != "y":
    return "n"
  if t[2] != chr(155):
    return "n"
  return "y"
def isutfrightsingle(t):
  if isutf80prefix(t) != "y":
    return "n"
  if t[2] != chr(153):
    return "n"
  return "y"
def isutfdash(t):
  if isutf80prefix(t) != "y":
    return "n"
  if t[2] != chr(148):
    return "n"
  return "y"
def isutfminus(t):
  if isutf80prefix(t) != "y":
    return "n"
  if t[2] != chr(147):
    return "n"
  return "y"
def isutftrademark(t):
  if isutf84prefix(t) != "y":
    return "n"
  if t[2] != chr(162):
    return "n"
  return "y"
  
def isutfdots(t):
  if isutf80prefix(t) != "y":
    return "n"
  if t[2] != chr(166):
    return "n"
  return "y"

# Following just for a unique single-right-quote case.
def maybeinsertnonbreakspace(outtoks,linetoks,nexttoknumin,lasttoknum):
  """ after the word 'variables' and a quote, insert non break space
  so things look ok. Bit of a hack to take care of one case. """
  # Check 2 since it is counting the one after current and
  # we look before current.
  if nexttoknumin < 2:
    return
  t = linetoks[nexttoknumin-2]
  rawtok = ''.join(t._tex)
  if rawtok != "variables":
    return
  t1=fileio.dwtoken()
  t1.setInitialOther("\\")
  t1.setNextOther(" ")
  append_to_out(outtoks,[t1])
  
def maybeinsertspace(outtoks,linetoks,nexttoknumin,lasttoknum):
  if nexttoknumin > lasttoknum:
    return
  t = linetoks[nexttoknumin]
  rawtok = ''.join(t._tex)
  if rawtok[0] == " ":
    return
  t1=fileio.dwtoken()
  t1.setIndivid(" ")
  append_to_out(outtoks,[t1])
  return
def transfunc(linetoks,myfile,linenum):
  if len(linetoks) < 1:
    return linetoks
  tnumin = 0
  changes = 0
  lasttoknum = len(linetoks) -1
  outtoks = []
  nexttoknumin = 0 
  for t in linetoks:
    nexttoknumin = nexttoknumin + 1
    rawtok = ''.join(t._tex)
    #stdname= ''.join(t._std)
    #linkname = "chap:" + ''.join(t._label)
    if len(rawtok) == 3:
        if isutfleftdouble(rawtok) == "y":
            t1=fileio.dwtoken()
            t1.insertid("\\doublequote")
            t2=fileio.dwtoken()
            t2.setIndivid("{")
            append_to_out(outtoks,[t1])
            append_to_out(outtoks,[t2])
            changes = changes +  1
        elif isutfrightdouble(rawtok) == "y":
            t4=fileio.dwtoken()
            t4.setIndivid("}")
            append_to_out(outtoks,[t4])
            changes = changes +  1
        elif isutfleftsingle(rawtok) == "y":
            # Here, odd trailing space is so next char does not hit
            # following word in output.
            # Sometimes quote right single is in a contraction
            # not part of a pair, so we don't try to pair them
            # here with\singlequote{}
            t1=fileio.dwtoken()
            t1.insertid("\\textquoteleft")
            append_to_out(outtoks,[t1])
            maybeinsertspace(outtoks,linetoks,nexttoknumin,lasttoknum)
            changes = changes +  1
        elif isutfrightsingle(rawtok) == "y":
            t1=fileio.dwtoken()
            t1.insertid("\\textquoteright")
            append_to_out(outtoks,[t1])
            maybeinsertnonbreakspace(outtoks,linetoks,nexttoknumin,lasttoknum)
            maybeinsertspace(outtoks,linetoks,nexttoknumin,lasttoknum)
            changes = changes +  1
        elif isutfdash(rawtok) == "y":
            t1=fileio.dwtoken()
            t1.insertid("\\textemdash" )
            append_to_out(outtoks,[t1])
            maybeinsertspace(outtoks,linetoks,nexttoknumin,lasttoknum)
            changes = changes +  1
        elif isutfminus(rawtok) == "y":
            t1=fileio.dwtoken()
            t1.insertid("\\textendash")
            append_to_out(outtoks,[t1])
            maybeinsertspace(outtoks,linetoks,nexttoknumin,lasttoknum)
            changes = changes +  1
        elif isutftrademark(rawtok) == "y":
            # Force a non-break space after the TM symbol
            # so the output has a space for real.
            t1=fileio.dwtoken()
            t1.insertid("\\texttrademark\\ ")
            append_to_out(outtoks,[t1])
            maybeinsertspace(outtoks,linetoks,nexttoknumin,lasttoknum)
            changes = changes +  1
        elif isutfdots(rawtok) == "y":
            t1=fileio.dwtoken()
            t1.insertid("\\dots")
            append_to_out(outtoks,[t1])
            maybeinsertspace(outtoks,linetoks,nexttoknumin,lasttoknum)
            changes = changes +  1
        else:
            outtoks += [t]
    else:
      outtoks += [t]
    tnumin = tnumin+ 1
    # End of for loop.
  return outtoks

def process_files(filelist):
  dwf = fileio.readFilelist(filelist)
  dwf.dwtransformline(transfunc)
  dwf.dwwrite()

def read_all_args():
  filelist = []
  cur = 1
  while  len(sys.argv) > cur:
    v = sys.argv[cur]
    filelist += [v]
    cur = int(cur) + 1
  if len(filelist) < 1:
    print >> sys.stderr , "No files specified."
    sys.exit(1)
  process_files(filelist)

#  anylink [-t <class>] ... [file] ...

if __name__ == '__main__':
  read_all_args()

