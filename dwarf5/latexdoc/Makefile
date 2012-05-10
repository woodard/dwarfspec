
# Just using pdflatex will not work, the diagrams
# in the section-relationships appendix will not
# show up.
# Do latex multiple times to generate all the references
# completely.  Apparently the worst case (TOC using
# regular page numbers beginning at 1) 
# up to 4 times might be needed.
# You need to do makeindex before the final latex!
all:
	latex dwarf5.tex
	latex dwarf5.tex
	makeindex dwarf5
	latex dwarf5.tex
	latex dwarf5.tex
	dvips dwarf5.dvi -o dwarf5.ps
	ps2pdf dwarf5.ps dwarf5.pdf
clean:
	-rm -f *.dvi
	-rm -f *.aux
	-rm -f *.idx
	-rm -f *.ilg
	-rm -f *.ind
	-rm -f *.toc
	-rm -f *.log
	-rm -f *.lof
	-rm -f *.lot
	-rm -f *.out
	-rm -f *.ps
	-rm -f p2.txt
archive:
	sh bldtar.sh
        

	

