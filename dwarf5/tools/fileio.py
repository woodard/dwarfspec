
# All the little classes used in storing latex source data.
# Copyright 2012 DWARF Debugging Information Format Committee

import sys

def isIdStart(c):
  if isIndivid(c) == "y":
    return "n"
  if  ord(c) >= ord('a') and ord(c) <= ord('z'):
    return "y"
  if  ord(c) >= ord('A') and ord(c) <= ord('Z'):
    return "y"
  # It is tex/latex, so backslash starts a word.
  if c == "\\":
    return "y"
  if c == "_":
    return "y"
  return "n"

def isIdNext(c):
  if isIndivid(c) == "y":
    return "n"
  if  ord(c) >= ord('a') and ord(c) <= ord('z'):
    return "y"
  if  ord(c) >= ord('A') and ord(c) <= ord('Z'):
    return "y"
  if  ord(c) >= ord('0') and ord(c) <= ord('9'):
    return "y"
  # This is so we allow the colon in our tags
  if c == ":":
    return "y"
  if c == "\\":
    return "y"
  if c == "-":
    return "y"
  if c == "_":
    return "y"
  return "n"
def isIndivid(c):
  if c == "[":
    return "y"
  if c == "]":
    return "y"
  if c == "{":
    return "y"
  if c == "}":
    return "y"
  if c == " ":
    return "y"
  if c == "\t":
    return "y"
  return "n"

class dwtoken:
  def __init__(self):
    self._tex = []
    self._underbar = []
    self._std = []
    self._label = []
    # Class is "id", "ind","other","none"
    self._class = "none"
  def insertid(self,string):
    self._class =  "id"
    self._tex = list(string)
    self._underbar = self._tex
    self._std = self._tex
    self._label = self._tex
  def setIndivid(self,c):
    self._tex = [c]
    self._underbar = [c]
    self._std = [c]
    self._label = [c]
    self._class =  "ind"
  def setInitialIdChar(self,c):
    self._tex = [c]
    self._class =  "id"
  def setNextIdChar(self,c):
    self._tex += [c]

  def setInitialOther(self,c):
    self._tex = [c]
    self._underbar = [c]
    self._std = [c]
    self._label = [c]
    self._class =  "other"
  def setNextOther(self,c):
    self._tex += [c]
    self._underbar += [c]
    self._std += [c]
    self._label += [c]
    self._class =  "other"
  def finishUpId(self):
    """ This transforms the strings from the input form into
        the internal forms we want.
    """
    self._underbar = []
    self._std = []
    self._label = []
    n = 0
    # Drop \-
    while int(n) < len(self._tex):
      c = self._tex[n]
      if n < (len (self._tex) - 1) and c == "\\" and self._tex[n+1] == "-":
        n = n +2
        continue
      self._underbar += [c]
      n = n +1
    # Drop \ from \_
    n = 0
    while int(n) < len(self._underbar):
      c = self._underbar[n]
      if n < (len (self._underbar) - 1) and c == "\\" and self._underbar[n+1] == "_":
        n = n +1
        continue
      self._std += [c]
      n = n +1
    # Drop  underbar
    n = 0
    while int(n) < len(self._std):
      c = self._std[n]
      if  c == "_":
        n = n +1
        continue
      self._label += [c]
      n = n +1

  def dwprintquotedshortform(self,d):
      print "'",self.shortform(d),"'",
  def shortform(self,d):
      return ''.join(d)
  def dwprint(self):
    if self._class == "ind":
      print self._class, 
      self.dwprintquotedshortform(self._tex)
      print ""
    else:
      # This prints the token with end-line oddly.
      print self._class, 
      self.dwprintquotedshortform(self._tex)
      self.dwprintquotedshortform(self._underbar)
      self.dwprintquotedshortform(self._std)
      self.dwprintquotedshortform(self._label)
      print ""
  def dwwrite(self,outfile):
    for x in self._tex:
      outfile.write(x)

class  dwline:
  """using an input line, create a list of tokens for the line.
     Legal class transitions in tokenize() are:
     none->other
     none->id
     none->ind
     other->ind
     other->id
     id->ind
     id->other
  """
  def __init__(self):
    # list of dwtoken.
    self._toks = []

  
  def tokenize(self,rec):
    """using an input line, create a list of tokens for the line.
       Legal class transitions in tokenize() are:
       none->other
       none->id
       none->ind
       other->ind
       other->id
       id->ind
       id->other
    """
    dwclass = "none"
    combotok = dwtoken()
    for c in rec:
      if c == "\n" or c == "\r":
          # Just drop these for now. Allowing them
          # would not be harmful.
          continue
      elif dwclass == "none" or dwclass == "ind":
        if isIndivid(c) == "y":
          a = dwtoken()
          a.setIndivid(c);
          self._toks += [a]
          continue
        if isIdStart(c) == "y":
          combotok.setInitialIdChar(c)
          dwclass = "id"
          continue
        # is "other"
        combotok.setInitialOther(c)
        dwclass = "other"
        continue
      elif dwclass == "id": 
        if isIdNext(c) == "y":
          combotok.setNextIdChar(c)
          continue
        if isIndivid(c) == "y":
          combotok.finishUpId()
          self._toks += [combotok]
          combotok = dwtoken()
          a = dwtoken()
          a.setIndivid(c);
          dwclass = "ind"
          self._toks += [a]
          continue
        # Other class input, other starts here.
        combotok.finishUpId()
        self._toks += [combotok]
        combotok = dwtoken()
        combotok.setInitialOther(c);
        dwclass = "other"
        continue
      elif dwclass == "other":
        if isIndivid(c) == "y":
          self._toks += [combotok]
          combotok = dwtoken()
          a = dwtoken()
          a.setIndivid(c);
          dwclass = "ind"
          self._toks += [a]
          continue
        if isIdStart(c) == "y":
          self._toks += [combotok]
          combotok = dwtoken()
          combotok.setInitialIdChar(c);
          dwclass = "id"
          continue
        combotok.setNextOther(c);
        continue
      # Else case impossible.
     
    #Finish up final non-empty other or id token
    if dwclass == "id":
      combotok.finishUpId()
      self._toks += [combotok]
      dwclass = "none"
    if dwclass == "other":
      self._toks += [combotok]
      dwclass = "none"
  def dwprint(self,linenum):
    print "Number of tokens in line ",linenum," : ",len(self._toks)
    if len(self._toks) == 0:
      #Just print an empty line.
      print ""
    else:
      for t in self._toks:
        t.dwprint()
  def dwwrite(self, outfile, linenum):
    for t in self._toks:
      t.dwwrite(outfile)
    outfile.write("\n")
  def dwtransformline(self,callfunc):
    toks = callfunc(self._toks)
    self._toks = toks
    

class dwfile:
  def __init__(self,name):
    # list of dwline.
    self._name = name
    # Name of the file.
    self._lines = []
    try:
      file = open(name,"r");
    except IOError, message:
      print >> sys.stderr , "File could not be opened: ", name
      sys.exit(1)
    while 1:
      try:
        rec = file.readline()
      except EOFError:
        break
      if len(rec) < 1:
        # eof
        break

      aline = dwline()
      aline.tokenize(rec)
      self._lines += [aline]

  def dwprint(self):
    print "Number of lines in ", self._name, ":  ",len(self._lines)
    lnum = 1
    for l in self._lines:
       l.dwprint(lnum)
       lnum = lnum + 1
  def dwwrite(self):
    # The lnum is just for debugging messages.

    outname = self._name + ".out"
    print outname
    try:
      outfile = open(outname,"w");
    except IOError, message:
      print >> sys.stderr , "Output File could not be opened: ", name
      sys.exit(1)
    lnum = 1
    for l in self._lines:
      l.dwwrite(outfile,lnum)
      lnum = lnum + 1
  def dwtransformline(self,callfunc):
    for l in self._lines:
      l.dwtransformline(callfunc)
    


class dwfiles:
  def __init__(self):
    # list of dwfile.
    self._files = []

  def addFile(self,name):
    f = dwfile(name)
    self._files += [f]
    
  def dwprint(self):
    print "Number of files: ",len(self._files);
    for f in self._files:
      f.dwprint()
  def dwwrite(self):
    for f in self._files:
      f.dwwrite()
  def dwtransformline(self,callfunc):
    for f in self._files:
      f.dwtransformline(callfunc)


def readFilelist(filelist):
  dwf = dwfiles()
  for f in filelist:
    dwf.addFile(f)
  return dwf

