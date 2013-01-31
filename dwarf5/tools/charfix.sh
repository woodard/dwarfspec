
m() {
    python charfix.py  ../latexdoc/$1
    mv ../latexdoc/$1.out ../latexdoc/$1
}
#m attributesbytag.tex	       
#m foreword4.1.tex 
m compression.tex		       
exit 0
m foreword.tex 
m copyright.tex		       
m generaldescription.tex dataobject.tex		       
m gnulicense.tex 
m datarepresentation.tex	       
m introduction.tex 
m debugsectionrelationships.tex  
m otherdebugginginformation.tex 
m dwarf5.tex		       
m programscope.tex 
m encodingdecoding.tex	       
m sectionversionnumbers.tex 
m examples.tex		       
m typeentries.tex
