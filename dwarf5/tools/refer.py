# Copyright 2014 DWARF Debugging Information Format Committee
#
# Looks at dwarfnamecmds.tex to find all the commands
# And sees what is actually used and whether references
# have definitions.
# The initial implemenation just *assumes* it is run from the tools
# directory and the file names are built in to the source here.
#
# Run as (for example)
#   python refer.py 


import sys
import fileio

# All the newdwfnamecommands
global dwfnamecommsdict
# All the newcommand instances.
global newcommsdict

# LINK suffix
global linksdict  

# TARG suffix hyperlink of 'chap:#1' Index #2
global targsdict
# INDX suffix index #2
global indxdict
# MARK suffix hypertarget chap:#1  and index #2
global markdict

# NAME suffix. No index, just text shows.
global namedict

# This is the 'normal, most common case in running text.
# Default implies index #2 and hyperlink of chap:#1
global defaultdict 

# Targets for \hypertarget and livetarg[i]
global targhyperdict
# Links using hyperlink.
global linkhyperdict

# label targets (labels)
global labeldict
# \refersec \ref \vref to labels
global labelrefdict

# The index content for named things.
global indexdict


newcommsdict = {}
dwfnamecommsdict = {}

# Links meaning \livelink \livetarg \livetargi macros
linksdict  = {}
targsdict  = {}
indxdict  = {}
markdict  = {}
namedict  = {}
defaultdict  = {}
targhyperdict= {}
linkhyperdict= {}
labeldict = {}
labelrefdict = {}
indexdict = {}

global linestoignore
linestoignore = []

# lines_to_ignore is a terrible hack.
def add_lines_to_ignore(myfile,lowline,highline):
  global linestoignore
  linestoignore += [(myfile._name,lowline,highline)]
def in_lines_to_ignore(myfile,line):
  global linestoignore
  n = myfile._name
  for x in linestoignore:
    (n,l,h) = x
    if  myfile._name != n:
      continue
    if line < l:
      continue
    if line >h:
      continue
    return "y"
  return "n"
   

# a list of words to ignore: silly stuff.
ignorethesedict = {"of":0, "a":0, "the":0, "and":0, "but":0,"DWARF":0,
"Standards":0,"Committee":0,"Version":0 }

class tokmention:
  def __init__(self):
    self._token = '' 
    self._file = ""
    self._line = 0
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

def toknamestring(t):
  """ Turn a token into its string as a string """
  return ''.join(t._tex)


def pickup(linetoks,tnumin,pattern,myfile,linenum):
  """ The token pattern characters are
  i meaning identifier
  e meaning identifier, but ifnext token is }
     we construct an empty identifier for it.
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
    elif c == "e":
      if curtok._class != "id":
        if isbrace(curtok,"}") == "y":
          tk = fileio.dwtoken()
          tk.insertid("")
          outtoks += [tk]
          # Do not update location.
          continue
        else:
          print "ERROR line  expected identifier got ",curtok._tex, "pattern" , pattern, " line " ,linenum," file ",myfile._name
          return outtoks,numabsorbed
      else: 
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
    elif c == "[":
      if isbrace(curtok,"[")  == "y":
        outtoks += [curtok]
        curnum = curnum + 1
        numabsorbed = numabsorbed + 1
      else:
        print "ERROR line  expected [  got ",curtok._tex," pattern ",pattern," line " ,linenum," file ",myfile._name
        return outtoks,numabsorbed
    elif c == "]":
      if isbrace(curtok,"]")  == "y":
        outtoks += [curtok]
        curnum = curnum + 1
        numabsorbed = numabsorbed + 1
      else:
        print "ERROR line  expected ]  got ",curtok._tex," pattern ",pattern," line " ,linenum," file ",myfile._name
        return outtoks,numabsorbed
    elif c == "*":
      outlist = []
      curtok = linetoks[curnum]
      while isbrace(curtok,"}") == "n" and isbrace(curtok,"]") == "n":
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

def printbadcommand(name,myfile,myline):
  print "Error: command %s missing operand file %s line %d" %(name,myfile._name,myline)

def applytodict(d,k,v):
  keystring = k
  if d.has_key(keystring) == 0:
     d[keystring] =  [v]
  else:
     # This is a duplicate entry.
     # We will report on it later as appropriate.
     existing = d.get(keystring)
     existing += [v]
     d[keystring] =  existing

# See how many "{" there are on the line.
# return the count.
def countbraces(linetoks,tnumin):
  lasttoknum = len(linetoks) -1
  lb = 0
  while tnumin < lasttoknum:
    x = linetoks[tnumin] 
    if x._class == "ind":
       n = toknamestring(x)
       if n == "{":
          lb = lb + 1
    tnumin = tnumin + 1
  return lb
     


def processbegin(linetoks,tnumin,myfile,linenum):
  global targhyperdict
  global indexdict
  lbracecount = countbraces(linetoks,tnumin)
  if lbracecount < 3:
    return 1
  ourtoks,inlen = pickup(linetoks,tnumin," i { i } [ * ] { * } { i }",myfile,linenum)
  if len(ourtoks) < 12:
    return 1
  lcom = ourtoks[2]
  lcomname = toknamestring(lcom)
  if lcomname != "simplenametable":
    return inlen
  targ = ourtoks[11]
  hypstr = toknamestring(targ)
  hypmen = tokmention(targ,myfile,linenum)
  applytodict(labeldict,hypstr,hypmen)
  return inlen

# If justlink == "y" this is a hypertarget command literally.
def livetargprocess(linetoks,tnumin,myfile,linenum,justlink):
  """ \livetarg{chap:DWTAGtemplatevalueparameter}{DWTAGtemplatevalueparameter} """
  global targhyperdict
  global indexdict
  t = linetoks[tnumin]
  ourtoks,inlen = pickup(linetoks,tnumin,"i { i } { * }",myfile,linenum)
  if len(ourtoks) > 5:
    t2 = ourtoks[2];
    index = tokmention(t2,myfile,linenum)
    name = toknamestring(t2)
    applytodict(targhyperdict,name,index)
    if justlink == "n":
      t2 = ourtoks[5];
      # Ignore for now.
      #name = toknamestring(t2)
      #if len(name) > 0:
      #  index = tokmention(t2,myfile,linenum)
      #  applytodict(indexdict,name,index)
  else:
    tn = toknamestring(linetoks[tnumin])
    printbadcommand(tn,myfile,linenum)
  return inlen
def livetargiprocess(linetoks,tnumin,myfile,linenum):
  """ \livetargi{chap:DWTAGtemplatevalueparameter}{DW\-\_TAG\-\_template\-\_value\-\_parameter}{name of targ} """
  global targhyperdict
  global indexdict
  t = linetoks[tnumin]
  ourtoks,inlen = pickup(linetoks,tnumin,"i { i } { e } { * }",myfile,linenum)
  if len(ourtoks) > 5:
    t2 = ourtoks[2];
    index = tokmention(t2,myfile,linenum)
    name = toknamestring(t2)
    applytodict(targhyperdict,name,index)

    t2 = ourtoks[5];
    name = toknamestring(t2)
    if len(name) > 0:
      index = tokmention(t2,myfile,linenum)
      applytodict(indexdict,name,index)
  else:
    tn = toknamestring(linetoks[tnumin])
    printbadcommand(tn,myfile,linenum)
  return inlen
# if justlink == "y" it is a plain hyperlinkcommand
def livelinkprocess(linetoks,tnumin,myfile,linenum,justlink):
  """ \livelink{chap:DWTAGtemplatevalueparameter}{DW\-\_TAG\-\_template\-\_value\-\_parameter} """
  global linkhyperdict
  global indexdict
  t = linetoks[tnumin]
  ourtoks,inlen = pickup(linetoks,tnumin,"i { i } { * }",myfile,linenum)
  if len(ourtoks) > 5:
    t2 = ourtoks[2];
    index = tokmention(t2,myfile,linenum)
    name = toknamestring(t2)
    applytodict(linkhyperdict,name,index)

    # can be multiword. For now do not bother with every index.
    #t2 = ourtoks[5];
    #index = tokmention(t2,myfile,linenum)
    #name = toknamestring(t2)
    #applytodict(indexdict,name,index)
  else:
    tn = toknamestring(linetoks[tnumin])
    printbadcommand(tn,myfile,linenum)
  return inlen
def labelprocess(linetoks,tnumin,myfile,linenum):
  """ \label{alabel} """
  global labeldict
  t = linetoks[tnumin]
  ourtoks,inlen = pickup(linetoks,tnumin,"i { i }",myfile,linenum)
  if len(ourtoks) > 2:
    t2 = ourtoks[2];
    index = tokmention(t2,myfile,linenum)
    name = toknamestring(t2)
    applytodict(labeldict,name,index)
  else:
    tn = toknamestring(linetoks[tnumin])
    printbadcommand(tn,myfile,linenum)

  return inlen
def addtoindexprocess(linetoks,tnumin,myfile,linenum):
  """ \addtoindex{strings} """
  global indexdict
  ourtoks,inlen = pickup(linetoks,tnumin,"i { * }",myfile,linenum)
  if len(ourtoks) > 2:
    # The * means a list of tokens.
    fake = ""
    #t2 = ourtoks[2];
    #index = tokmention(t2,myfile,linenum)
    #name = toknamestring(t2)
    #applytodict(indexdict,name,index)
  else:
    tn = toknamestring(linetoks[tnumin])
    printbadcommand(tn,myfile,linenum)
  return inlen
def hyperlinkname(name,tnumin,myfile,linenum):
  global linkhyperdict
  tkmod = fileio.dwtoken()
  tkmod.insertid(name)
  tm = tokmention(tkmod,myfile,linenum)
  applytodict(linkhyperdict,name,tm)
  return 1
def hyperlinkprocess(linetoks,tnumin,myfile,linenum):
  """ \hyperlink{entryname} """
  global linkhyperdict
  ourtoks,inlen = pickup(linetoks,tnumin,"i { i }",myfile,linenum)
  if len(ourtoks) > 2:
    t2 = ourtoks[2];
    index = tokmention(t2,myfile,linenum)
    name = toknamestring(t2)
    applytodict(linkhyperdict,name,index)
  else:
    tn = toknamestring(linetoks[tnumin])
    printbadcommand(tn,myfile,linenum)
  return inlen

def indexprocess(linetoks,tnumin,myfile,linenum):
  """ \index{indexentryname} """
  global indexdict
  ourtoks,inlen = pickup(linetoks,tnumin,"i { * }",myfile,linenum)
  if len(ourtoks) > 2:
    fake = ""
    # For now not bothering with index strings
    #t2 = ourtoks[2];
    #index = tokmention(t2,myfile,linenum)
    #name = toknamestring(t2)
    #applytodict(indexdict,name,index)
  else:
    tn = toknamestring(linetoks[tnumin])
    printbadcommand(tn,myfile,linenum)
  return inlen
def refersecprocess(linetoks,tnumin,myfile,linenum):
  """ \refersec{label} """
  global labelrefdict
  t = linetoks[tnumin]
  ourtoks,inlen = pickup(linetoks,tnumin,"i { i }",myfile,linenum)
  if len(ourtoks) > 2:
    t2 = ourtoks[2];
    index = tokmention(t2,myfile,linenum)
    name = toknamestring(t2)
    applytodict(labelrefdict,name,labelrefdict)
  else:
    tn = toknamestring(linetoks[tnumin])
    printbadcommand(tn,myfile,linenum)
  return inlen

def firstnonblank(linetoks):
  tnum = 0
  lasttoknum = len(linetoks)
  while tnum < lasttoknum:
    x = linetoks[tnum]
    if x._class != "ind":
      return tnum
    if toknamestring(x) == " ":
      tnum = tnum + 1
      continue
    elif toknamestring(x) == "\t":
      tnum = tnum + 1
      continue
    return tnum 
  return tnum
# Deals solely with finding new commands.
# This done as a first pass so we can recognize when tokens are
# really commands, something transfunc2, the second pass, 
# wants to know. 
def transfunc1(linetoks,myfile,linenum):
  global dwfnamecommsdict
  global newcommsdict

  if len(linetoks) < 1:
    return linetoks
  tnum = firstnonblank(linetoks)
  if tnum >= len(linetoks):
    return linetoks
  initialtok = linetoks[tnum]
  itokstring=toknamestring(initialtok)
  if itokstring == "\\expandafter\\def\\csname":
    return linetoks
  if in_lines_to_ignore(myfile,linenum) == "y":
    return linetoks
  if itokstring == "\\newcommand":
    t1 = linetoks[tnum+1]
    if not isbrace(t1,'{'):
      print "Improper character in newcommand", myfile,linenum
      sys.exit(1)
    t2 = linetoks[tnum+2]
    if toknamestring(t2) == "\\simplenametablerule":
       add_lines_to_ignore(myfile,linenum,linenum+18)
    if toknamestring(t2) != "\\newdwfnamecommands":
       tm = tokmention(t2,myfile,linenum)
       applytodict(newcommsdict,toknamestring(t2),tm)
    #Be silent on newdwfnamecommands, it is normal.
    #else:
    #   print "newcommand on newdwfnamecommands ignored intentionally."
    return linetoks
  elif itokstring == "\\newdwfnamecommands":
    t1 = linetoks[tnum+1]
    if not isbrace(t1,'{'):
       print "Improper character in newdwfnamecommands", myfile._name,linenum
       sys.exit(1)
    # The token name string will be DWsomething and we want
    # The token to appear as \DWsomething as that is how references
    # The usages determine what secondary actions are applied.
    # are coded.
    t2 = linetoks[tnum+2]
    tkmod = fileio.dwtoken()
    tkmod.insertid("\\" + toknamestring(t2))
    tm = tokmention(tkmod,myfile,linenum)
    applytodict(dwfnamecommsdict,toknamestring(tkmod),tm)
    return linetoks
  return linetoks


def delsuffix(n,suf):
  slen = len(suf)
  nlen = len(n)
  lastcharnum = nlen - slen
  outstring = n[0:lastcharnum]
  return outstring
def deloptionalprefix(n,pref):
  if not n.startswith(pref):
    return n
  plen = len(pref)
  nlen = len(n)
  outstring = n[plen:nlen]
  return outstring

def printodderr(rawname,comname,myfile,linenum):
  print "Error: this looks like a command is missing: ",rawname,"tested as",comname," in ",myfile._name," at ",linenum

def rawnameiscommand(t,suff):
   if not t.startswith("\\DW"):
     return ""
   if not t.endswith(suff):
     return ""
   commandname = delsuffix(t,suff)
   return commandname

# Delete any leading backslash.
# Prefix the result with chap:
def makelinkname(t):
   s = deloptionalprefix(t,"\\");
   s2 = "chap:" + s
   return s2;
   

# Assumes all new commands known already.
# This deals with targets and links (various flavors).
def transfunc2(linetoks,myfile,linenum):
  global newcommsdict
  global dwfnamecommsdict
  global newcommsdict

  # Link naming target
  global linksdict
  # TARG suffix
  global targsdict
  # INDX suffix
  global indxdict
  # MARK suffix
  global markdict
  # NAME suffix
  global namedict
  # This is the 'normal, most common case in running text.
  global defaultdict

  if len(linetoks) < 1:
    return linetoks
  if in_lines_to_ignore(myfile,linenum) == "y":
    return linetoks
  initialtok = linetoks[0]
  itokstring=toknamestring(initialtok)
  # Skip all the newcommand stuff.
  if itokstring == "\\newcommand":
    return linetoks
  elif itokstring == '\\newdwfnamecommands':
    return linetoks

  # Now deal with a regular line.

  tnumin = 0
  changes = 0
  lasttoknum = len(linetoks) -1
  for x in linetoks:
    if int(tnumin) > int(lasttoknum):
      break
    t = linetoks[tnumin]
    if t._class != "id":
      tnumin = tnumin + 1
      continue
    rawname = toknamestring(t)
    commandname=""
    #rawnameiscommand(rawname,"",basecommand)
    if rawname == "\\expandafter\\def\\csname":
      return linetoks
    if rawname == "\\begin":
      tnumcount = processbegin(linetoks,tnumin,myfile,linenum);
      tnumin = tnumin + tnumcount
      continue
    if dwfnamecommsdict.has_key(rawname):
      # We know this one. 
      # It is a default case name reference.
      # index the DWname
      # Link is to chap:DWname
      tm = tokmention(t,myfile,linenum)
      applytodict(defaultdict,rawname,tm)
      linkname = makelinkname(rawname)
      indxname = deloptionalprefix(commandname,"\\")
      applytodict(linkhyperdict,linkname,tm);
      applytodict(indexdict,indxname,tm);
      tnumin = tnumin + 1
      continue
    if  newcommsdict.has_key(rawname):
      # We know this one. We have to see what it is
      # To decide what to do.
      # some DWOPbreg*  DWOPreg*   and MDfive are special.
      # A variety of other such defined commands are irrelevant to us here.

      tnumcount = 1
      if rawname == "\\livetarg":
        tnumcount = livetargprocess(linetoks,tnumin,myfile,linenum,"n")
      elif rawname == "\\livetargi":
        tnumcount = livetargiprocess(linetoks,tnumin,myfile,linenum)
      elif rawname == "\\livelink":
        tnumcount = livelinkprocess(linetoks,tnumin,myfile,linenum,"n")
      elif rawname == "\\livelinki":
        tnumcount = livelinkprocess(linetoks,tnumin,myfile,linenum,"n")
      #elif rawname == "\\label":
      #  tnumcount = labelprocess(linetoks,tnumin,myfile,linenum)
      elif rawname == "\\refersec":
        # does \ref
        tnumcount = refersecprocess(linetoks,tnumin,myfile,linenum)
      elif rawname == "\\referfol":
        # does \vref from varioref package
        tnumcount = refersecprocess(linetoks,tnumin,myfile,linenum)
      elif rawname == "\\index":
        tnumcount = indexprocess(linetoks,tnumin,myfile,linenum)
      elif rawname == "\\addtoindex":
        tnumcount = indexprocess(linetoks,tnumin,myfile,linenum)
      elif rawname == "\\addtoindexx":
        tnumcount = indexprocess(linetoks,tnumin,myfile,linenum)
      elif rawname == "\\addttindex":
        tnumcount = indexprocess(linetoks,tnumin,myfile,linenum)
      elif rawname == "\\addttindexx":
        tnumcount = indexprocess(linetoks,tnumin,myfile,linenum)
      elif rawname == "\\DWOPbregtwo":
        tnumcount = hyperlinkname("chap:DWOPbregn",tnumin,myfile,linenum)
      elif rawname == "\\DWOPbregthree":
        tnumcount = hyperlinkname("chap:DWOPbregn",tnumin,myfile,linenum)
      elif rawname == "\\DWOPbregfour":
        tnumcount = hyperlinkname("chap:DWOPbregn",tnumin,myfile,linenum)
      elif rawname == "\\DWOPbregfive":
        tnumcount = hyperlinkname("chap:DWOPbregn",tnumin,myfile,linenum)
      elif rawname == "\\DWOPbregeleven":
        tnumcount = hyperlinkname("chap:DWOPbregn",tnumin,myfile,linenum)
      elif rawname == "\\MDfive":
        tnumcount = hyperlinkname("def:MDfive",tnumin,myfile,linenum)
      else:
        fake = ""
        # If missing anything important, perhaps turn ths on.
        #print "Error not handled: %s in file %s line %d" %(rawname,myfile._name,linenum)
      tnumin = tnumin + tnumcount
      continue
    # Suffixes are LINK TARG INDX MARK NAME
    commandname =rawnameiscommand(rawname,"LINK")
    if len(commandname) > 0:
      # We do not expect to see this in text, LINK is really how
      # the defaultdict entries are created so should
      # be hidden from us here.
      # index the DWname
      # Link is to chap:DWname
      if dwfnamecommsdict.has_key(commandname):
        tm = tokmention(t,myfile,linenum)
        linkname = makelinkname(commandname)
        indxname = deloptionalprefix(commandname,"\\")
        applytodict(linkhyperdict,linkname,tm)
        applytodict(indexdict,indxname,tm);
      else:
        printodderr(rawname,commandname,myfile,linenum)
      tnumin = tnumin + 1
      continue
    commandname =rawnameiscommand(rawname,"TARG")
    if len(commandname) > 0:
      # index DWname
      # Set chap:DWname as having target defined
      if dwfnamecommsdict.has_key(commandname):
        tm = tokmention(t,myfile,linenum)
        targname = makelinkname(commandname)
        indxname = deloptionalprefix(commandname,"\\")
        applytodict(targsdict,targname,tm)
        applytodict(indexdict,indxname,tm);
      else:
        printodderr(rawname,commandname,myfile,linenum)
      tnumin = tnumin + 1
      continue
    commandname =rawnameiscommand(rawname,"INDX")
    if len(commandname) > 0:
      # Index DWname
      if dwfnamecommsdict.has_key(commandname):
        tm = tokmention(t,myfile,linenum)
        indexname = deloptionalprefix(commandname,"\\")
        applytodict(indxdict,indexname,tm)
      else:
        printodderr(rawname,commandname,myfile,linenum)
      tnumin = tnumin + 1
      continue
    commandname =rawnameiscommand(rawname,"MARK")
    if len(commandname) > 0:
      # set chap:DWname as target defined
      # index DWname
      if dwfnamecommsdict.has_key(commandname):
        tm = tokmention(t,myfile,linenum)
        applytodict(markdict,commandname,tm)
        indexname = deloptionalprefix(commandname,"\\")
        applytodict(indxdict,indexname,tm)
        targname = makelinkname(commandname)
        applytodict(markdict,targname,tm)
      else:
        printodderr(rawname,commandname,myfile,linenum)
      tnumin = tnumin + 1
      continue
    commandname =rawnameiscommand(rawname,"NAME")
    if len(commandname) > 0:
      # No actions with NAME (but put in namedict anyway).
      if dwfnamecommsdict.has_key(commandname):
        tm = tokmention(t,myfile,linenum)
        applytodict(namedict,commandname,tm)
      else:
        printodderr(rawname,commandname,myfile,linenum)
      tnumin = tnumin + 1
      continue
    if rawname == "\\label":
      # This is a builtin, not our newcommand.
      tnumcount = labelprocess(linetoks,tnumin,myfile,linenum)
      tnumin = tnumin + tnumcount
      continue
    if rawname == "\\hypertarget":
      # This is a builtin, not our newcommand.
      tnumcount = livetargprocess(linetoks,tnumin,myfile,linenum,"y")
      tnumin = tnumin + tnumcount
      continue
    if rawname == "\\hyperlink":
      # This is a builtin, not our newcommand.
      tnumcount = livelinkprocess(linetoks,tnumin,myfile,linenum,"y")
      tnumin = tnumin + tnumcount
      continue
    # Some random data or text here.

    tnumin = tnumin + 1
    # We don't know what this is. Probably ok?
    # End of for loop.
  return linetoks

def sort_tokmlist(mylist):
  aux = [ (''.join(x._token._tex),x) for x in mylist ]
  aux.sort()
  return[ (x[1]) for x in aux]

def printtokmention(ct,v):
  n = v._token
  name =  toknamestring(n)
  f = v._file
  l = v._line
  print "    [%2d] %s in file %s line %d" %(ct,name,f._name,l)

def printtoomany(name,k,vlist):
  print "Duplicate in %s: %s:" %(name,k)
  ct = 0
  for v in vlist:
      printtokmention(ct,v)
      ct = ct + 1

def checkduplicatetargs(dname,d):
  targs = d.items()
  for vi in targs:
    (k,v) = vi
    if len(v) > 1:
      printtoomany(dname,k,v)

def checkmissingtarg(name,targ,refs):
  rlist = refs.items()
  for r in rlist:
    (k,v) = r
    if targ.has_key(k) == 0:
       print "target missing from",name,":",k

def checkmissingref(name,targ,refs):
  rlist = targ.items()
  for r in rlist:
    (k,v) = r
    if refs.has_key(k) == 0:
       print "Unused target from",name,":",k
  
def print_stats():
  # All the newdwfnamecommands
  global dwfnamecommsdict
  # All the newcommand instances.
  global newcommsdict
  
  # LINK suffix
  global linksdict
  
  # TARG suffix hyperlink of 'chap:#1' Index #2
  global targsdict
  # INDX suffix index #2
  global indxdict
  # MARK suffix hypertarget chap:#1  and index #2
  global markdict
  # NAME suffix. No index, just text shows.
  global namedict
  # This is the 'normal, most common case in running text.
  # Default implies index #2 and hyperlink of chap:#1
  global defaultdict
  
  # Targets for \hypertarget and livetarg[i]
  global targhyperdict
  # Links using hyperlink.
  global linkhyperdict
  # label targets (labels)
  global labeldict
  # \refersec \ref \vref to labels
  global labelrefdict
  # The index content for named things.
  global indexdict
  
  checkduplicatetargs("targets",targsdict)
  checkduplicatetargs("hypertargets",targhyperdict)
  checkduplicatetargs("MARKs",markdict)
  checkduplicatetargs("newdwfname commands",dwfnamecommsdict)
  checkduplicatetargs("commands",newcommsdict)
  checkduplicatetargs("labels",labeldict)

  checkmissingtarg("hyperlinks",targhyperdict,linkhyperdict)
  checkmissingref("hyperlinks",targhyperdict,linkhyperdict)

  checkmissingtarg("labels",labeldict,labelrefdict)
  checkmissingref("labels",labeldict,labelrefdict)

  checkmissingref("names",dwfnamecommsdict,namedict)

debug = "n"
 
def read_all_args():
  filelist1 = []
  filelist2 = []
  fileio.setkeepordeletecomments("d")
  filelist1 = {"./testrefer.tex"}
  filelist2 = {"./testrefer.tex"}
  if debug == "n":
    filelist1 = {"../latexdoc/dwarfnamecmds.tex",
              "../latexdoc/dwarf5.tex",
              "../latexdoc/generaldescription.tex"}

    filelist2 = {"../latexdoc/dwarf5.tex",
              "../latexdoc/attributesbytag.tex",
              "../latexdoc/changesummary.tex",
              "../latexdoc/compression.tex",
              "../latexdoc/copyright.tex",
              "../latexdoc/dataobject.tex",
              "../latexdoc/datarepresentation.tex",
              "../latexdoc/debugsectionrelationships.tex",
              "../latexdoc/encodingdecoding.tex",
              "../latexdoc/examples.tex",
              "../latexdoc/foreword.tex",
              "../latexdoc/generaldescription.tex",
              "../latexdoc/gnulicense.tex",
              "../latexdoc/introduction.tex",
              "../latexdoc/otherdebugginginformation.tex",
              "../latexdoc/programscope.tex",
              "../latexdoc/sectionversionnumbers.tex",
              "../latexdoc/splitobjects.tex",
              "../latexdoc/typeentries.tex"}

  if (len(filelist1) < 1) or (len(filelist2) < 1):
    print >> sys.stderr , "No files specified to refer.py, internal error."
    sys.exit(1)
  # Pickup all the newcommand instances.
  dwf = fileio.readFilelist(filelist1)
  dwf.dwtransformline(transfunc1)

  # Now find all the uses.
  dwf2 = fileio.readFilelist(filelist2)
  dwf2.dwtransformline(transfunc2)
  print_stats()

if __name__ == '__main__':
  read_all_args()

