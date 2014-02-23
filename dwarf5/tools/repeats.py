# Copyright 2014 DWARF Debugging Information Format Committee
# This reads the a text file, usually
# the output of   pdftotext dwarf5.txt
# looks at each word in turn, keeping a window
# of words, looking for repeated words and short
# phrases

import sys

global checkwindow
checkwindow = []

# Eliminates lots of stuff 
# But allows plain numbers through.
def strisasciialpha(s):
  ok = "y"
  for c in s:
    if c >= 'a' and c <= 'z':
       continue
    elif c >= 'A' and c <= 'Z':
       continue
    # Pure numbers will be eliminated 
    # later
    elif c >= '0' and c <= '9':
       continue
    elif c == '-':
       continue
    elif c == '_':
       continue
    elif c == '\\':
       continue
    elif c == '/':
       continue
    else:
       return "n"
  return "y"

def checkdup(filename,line,checkwindow,phrasewindow,winlen,phraselen):
  iw = -1 
  winlen = len(checkwindow)
  phraselen = len(phrasewindow)
  # Numbers -- we claim we can never match
  for w in phrasewindow:
    if strisasciialpha(w) == "n":
      return "n"
    # If it is just a number, do not match
    try: float(w)
    except ValueError: continue 
    else: return "n"
  for winword in checkwindow:
    match = 0
    iw = iw + 1
    if (iw + phraselen) < winlen:
      ip = -1
      match = 0
      for pw in phrasewindow:
        ip = ip + 1
        if checkwindow[iw+ip] == phrasewindow[ip]:
          match = match +1
    if match == phraselen:
      print "duplicated: ",phrasewindow," file ", filename,"line",line
      return "y"
  return "n"
   
      
      
def updatewindow(winin,word,winlen):
   if len(winin) < winlen:
      out = winin + [word]
      return out
   if winlen == 1:
      out = [word]
      return out
   tmp = winin[1:]
   out = tmp + [word]
   return out

def procrecords(filename,recs,winlen,phraselen):
  global checkwindow
  phrasewindow = []
  curline=0
  for r in recs:
    curline = curline +1
    line = r.split()
    wdct = len(line)
    if wdct > 0:
      ct = 0
      while ct < wdct:
        w = line[ct]
        ct = ct + 1
        pw2 = updatewindow(phrasewindow,w,phraselen)
        phrasewindow = pw2
        if len(phrasewindow) < phraselen:
          pw3 = updatewindow(checkwindow,w,winlen)
          checkwindow = pw3
          continue
        res = checkdup(filename,curline,checkwindow,phrasewindow,winlen,phraselen)
        pw3 = updatewindow(checkwindow,w,winlen)
        checkwindow = pw3

def procfile(file,filename,winlen,phraselen):
  records = file.readlines()
  procrecords(filename,records,int(winlen),int(phraselen))
  

def read_args():
  cur = 1
  filelist = []
  if len(sys.argv) != 4:
    print "Expect 3 arguments N N <file>"
    sys.exit(1)
  
  w = sys.argv[1]
  p = sys.argv[2]
  if p > w :
    winlen = p
    phraselen = w
  else:
    phraselen = p
    winlen = w
  v = sys.argv[3]
  try:
      file = open(v,"r")
  except IOError:
      print "Unable to open ",v
      sys.exit(1)
  procfile(file,v,int(winlen),int(phraselen))

if __name__ == '__main__':
  read_args()
  


