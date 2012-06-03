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

global linkdefinitionsdict
global linkusesdict
global labeldefinitionsdict
global labelusesdict
global ignorethesedict
global indexsetdict
global dupdefcount
global unresolveddwdict
# Links meaning \livelink \livetarg \livetargi macros
linkdefinitionsdict = {}
linkusesdict  = {}
# labels meaning \refersec (a ref) and \label  (a def)
labeldefinitionsdict = {}
labelusesdict =  {}
# The dict of indexed things.
indexsetdict ={}
# DW sorts of names not sensibly resolved.
unresolveddwdict = {}
dupdefcount = 0



# a list of words to ignore: silly stuff.
ignorethesedict = {"of":0, "a":0, "the":0, "and":0, "but":0,"DWARF":0,
"Standards":0,"Committee":0,"Version":0 }

class tokmention:
  def __init__(self):
    self._token = '' 
    self._file = ""
    self._line = 0
    # Class is "id", "ind","other","none"
  def __init__(self,tok,filename,line):
    self._token = tok
    self._file = filename
    self._line = line




def ischar(tok,c):
   if tok._class != "ind":
      return "n"
   if len(tok._tex) != 1:
       return "n"
   if tok._tex[0] != c:
       return "n"
   return "y"

def dwspace(tok):
  if ischar(tok," ") == "y":
    return "y"
  if ischar(tok,"\t") == "y":
    return "y"
  return "n"
  
  
def isbrace(tok,brace):
  if tok._class != "ind":
     return "n"
  if len(tok._tex) != 1:
     return "n"
  if brace == tok._tex[0]:
     return "y"
  return "n"


def pickup(linetoks,tnumin,pattern,myfile,linenum):
  """ The token pattern characters are
  i meaning identifier
  [space] meaning whitespace
  { meaning left brace
  } meaning right brace
  * meaning any token except } and end-line
  
  Precondition:  linetoks[tnumin] is identifier (meaning a command)
  Returns: a token list, one per non-space in the pattern.
     For the *, the token is itself a list of whatever it contains.
  """
  outtoks = []
  numabsorbed = 1
  inlen = len(linetoks) 
  curnum = tnumin
  curtok = linetoks[curnum]
  outtoks += [curtok]
  patterncharnum = -1
  for c in pattern:
    patterncharnum = patterncharnum + 1
    if curnum >= inlen:
      print "ERROR line ended surprisingly, pattern ", pattern,"  line ",linenum," file ",myfile._name
      return outtoks,numabsorbed
    curtok = linetoks[curnum]
    if c == " ":
      while dwspace(curtok) == "y":
        curnum = curnum + 1
        if curnum >= inlen:
          print "ERROR line ended surprisingly in space, pattern ", pattern, " line ",linenum," file ",myfile._name
          return outtoks,numabsorbed
        numabsorbed = numabsorbed + 1
        curtok = linetoks[curnum]
      continue
    elif c == "i":
      if curtok._class != "id":
        print "ERROR line  expected identifier got ",curtok._tex, "pattern" , pattern, " line " ,linenum," file ",myfile._name
        return outtoks,numabsorbed
      numabsorbed = numabsorbed + 1
      outtoks += [curtok]
      curnum = curnum + 1
      continue
    elif c == "{":
      if isbrace(curtok,"{")  == "y":
        outtoks += [curtok]
        curnum = curnum + 1
        numabsorbed = numabsorbed + 1
      else:
        print "ERROR line  expected {  got ",curtok._tex," pattern ",pattern," line " ,linenum," file ",myfile._name
        return outtoks,numabsorbed
    elif c == "}":
      if isbrace(curtok,"}")  == "y":
        outtoks += [curtok]
        curnum = curnum + 1
        numabsorbed = numabsorbed + 1
      else:
        print "ERROR line  expected }  got ",curtok._tex,"pattern",pattern," line " ,linenum," file ",myfile._name
        return outtoks,numabsorbed
    elif c == "*":
      outlist = []
      curtok = linetoks[curnum]
      while isbrace(curtok,"}") == "n":
        if dwspace(curtok) == "n":
           outlist += [curtok]
        curnum = curnum + 1
        if curnum >= inlen:
          outtoks += [outlist]
          if patterncharnum < (len(pattern) -1): 
            print "ERROR insufficient tokens on line for pattern ", pattern," line " ,linenum," file ",myfile._name
          return outtoks,numabsorbed
        numabsorbed = numabsorbed + 1
        curtok = linetoks[curnum]
      # Found a right brace, so done here.
      outtoks += [outlist]
    else:
        print "ERROR pattern had unexpected character ",pattern
        sys.exit(1)
  return outtoks,numabsorbed

def reftodict(d,k,v):
  keystring = ''.join(k._token._tex)
  if d.has_key(keystring) == 0:
     d[keystring] =  [v]
  else:
     existing = d.get(keystring)
     existing += [v]
     d[keystring] =  existing

def deftodict(d,k,v):
  global dupdefcount
  keystring = ''.join(k._token._tex)
  if d.has_key(keystring) == 0:
     d[keystring] =  [v]
  else:
     # This is a duplication, we just record it here,
     # we will report on it shortly.
     dupdefcount = dupdefcount + 1
     existing = d.get(keystring)
     existing += [v]
     d[keystring] =  existing

def livetargprocess(linetoks,tnumin,myfile,linenum):
  """ \livetarg{chap:DWTAGtemplatevalueparameter}{DW\-\_TAG\-\_template\-\_value\-\_parameter} """
  global linkdefinitionsdict
  global linkusesdict
  global indexsetdict
  t = linetoks[tnumin]
  ourtoks,inlen = pickup(linetoks,tnumin,"i { i } { i }",myfile,linenum)
  if len(ourtoks) > 5:
    targlink= tokmention(ourtoks[2],myfile,linenum)
    targname= tokmention(ourtoks[5],myfile,linenum)
    deftodict(linkdefinitionsdict,targlink,targname)
    reftodict(indexsetdict,targname,targname)
  return inlen
def livetargiprocess(linetoks,tnumin,myfile,linenum):
  """ \livetargi{chap:DWTAGtemplatevalueparameter}{DW\-\_TAG\-\_template\-\_value\-\_parameter}{name of targ} """
  global linkdefinitionsdict
  global linkusesdict
  global indexsetdict
  t = linetoks[tnumin]
  ourtoks,inlen = pickup(linetoks,tnumin,"i { i } { i } { * }",myfile,linenum)
  if len(ourtoks) > 5:
    targlink= tokmention(ourtoks[2],myfile,linenum)
    targname= tokmention(ourtoks[5],myfile,linenum)
    deftodict(linkdefinitionsdict,targlink,targname)
    reftodict(indexsetdict,targname,targname)
  return inlen
def livelinkprocess(linetoks,tnumin,myfile,linenum):
  """ \livelink{chap:DWTAGtemplatevalueparameter}{DW\-\_TAG\-\_template\-\_value\-\_parameter} """
  global linkdefinitionsdict
  global linkusesdict
  global indexsetdict
  t = linetoks[tnumin]
  ourtoks,inlen = pickup(linetoks,tnumin,"i { i } { i }",myfile,linenum)
  if len(ourtoks) > 5:
    targlink= tokmention(ourtoks[2],myfile,linenum)
    targname= tokmention(ourtoks[5],myfile,linenum)
    reftodict(linkusesdict,targlink,targname)
    reftodict(indexsetdict,targname,targname)
  return inlen
def labelprocess(linetoks,tnumin,myfile,linenum):
  """ \label{alabel} """
  global labeldefinitionsdict
  t = linetoks[tnumin]
  ourtoks,inlen = pickup(linetoks,tnumin,"i { i }",myfile,linenum)
  if len(ourtoks) > 2:
    label = tokmention(ourtoks[2],myfile,linenum)
    deftodict(labeldefinitionsdict,label,label)
  return inlen
def addtoindexprocess(linetoks,tnumin,myfile,linenum):
  """ \addtoindex{alabel} """
  t = linetoks[tnumin]
  ourtoks,inlen = pickup(linetoks,tnumin,"i { i }",myfile,linenum)
  if len(ourtoks) > 2:
    index = tokmention(ourtoks[2],myfile,linenum)
    reftodict(indexsetdict,index,index)
  return inlen
def indexprocess(linetoks,tnumin,myfile,linenum):
  """ \index{indexentryname} """
  global labelusesdict
  t = linetoks[tnumin]
  ourtoks,inlen = pickup(linetoks,tnumin,"i { i }",myfile,linenum)
  if len(ourtoks) > 2:
    myentry = tokmention(ourtoks[2],myfile,linenum)
    reftodict(indexsetdict,myentry,myentry)
  return inlen
def refersecprocess(linetoks,tnumin,myfile,linenum):
  """ \refersec{label} """
  global labelusesdict
  t = linetoks[tnumin]
  ourtoks,inlen = pickup(linetoks,tnumin,"i { i }",myfile,linenum)
  if len(ourtoks) > 2:
    label = tokmention(ourtoks[2],myfile,linenum)
    reftodict(labelusesdict,label,label)
  return inlen

def transfunc(linetoks,myfile,linenum):
  if len(linetoks) < 1:
    return linetoks
  initialtok = linetoks[0]
  if ''.join(initialtok._tex) == "\\newcommand":
    # We ignore newcommand lines, they are not stuff
    # we want to look at, they are new macros, not macro uses.
    # We don't want to transform or touch them, nor report on them.
    return linetoks
  tnumin = 0
  lasttoknum = len(linetoks)
  while tnumin < lasttoknum:
    t = linetoks[tnumin]
    tnumcount = 1
    rawtok = ''.join(t._tex)
    stdname= ''.join(t._std)
    if rawtok == "\\livetarg":
      tnumcount = livetargprocess(linetoks,tnumin,myfile,linenum)
    elif rawtok == "\\livetargi":
      tnumcount = livetargiprocess(linetoks,tnumin,myfile,linenum)
    elif rawtok == "\\livelink":
      tnumcount = livelinkprocess(linetoks,tnumin,myfile,linenum)
    elif rawtok == "\\label":
      tnumcount = labelprocess(linetoks,tnumin,myfile,linenum)
    elif rawtok == "\\refersec":
      tnumcount = refersecprocess(linetoks,tnumin,myfile,linenum)
    elif rawtok == "\\addtoindex":
      tnumcount = addtoindexprocess(linetoks,tnumin,myfile,linenum)
    elif rawtok == "\\index":
      tnumcount = indexprocess(linetoks,tnumin,myfile,linenum)
    else:  
      if t._class == "id":
        namemention = tokmention(t,myfile,linenum)
        namestring = ''.join(t._std)
        if namestring.startswith("DW"):
          global unresolveddwdict
          reftodict(unresolveddwdict,namemention,namemention)
        # Else we might want to build a dict of all other words 
        # while leaving out all \latex commands we don't know?
    tnumin = tnumin + tnumcount
    # End of for loop.
  return linetoks

def process_files(filelist):
  dwf = fileio.readFilelist(filelist)
  # We will really just report, not transform
  # anything, but this works.
  dwf.dwtransformline(transfunc)

  # Here we report on our discoveries.

def read_file_args(targlist):
  cur = 1
  filelist = []
  while  len(sys.argv) > cur:
    v = sys.argv[cur]
    filelist += [v]
    cur = int(cur) + 1
  process_files(filelist)
  



def read_all_args():
  filelist = []
  fileio.setkeepordeletecomments("d")
  cur = 1
  while  len(sys.argv) > cur:
    v = sys.argv[cur]
    filelist += [v]
    cur = int(cur) + 1
  if len(filelist) < 1:
    print >> sys.stderr , "No files specified."
    printlegals()
    sys.exit(1)
  process_files(filelist)

#  anylink [-t <class>] ... [file] ...

if __name__ == '__main__':
  read_all_args()

