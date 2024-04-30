
# Just using pdflatex will not work, the diagrams
# in the section-relationships appendix will not
# show up.
# Do latex multiple times to generate all the references
# completely.  Apparently the worst case (TOC using
# regular page numbers beginning at 1) 
# up to 4 times might be needed.
# You need to do makeindex before the final latex!
# --driver=pdftex might be needed with the pdflatex command?
all:
	pdflatex -halt-on-error dwarf6.tex
	pdflatex -halt-on-error dwarf6.tex
	makeindex dwarf6
	pdflatex -halt-on-error dwarf6.tex
	pdflatex -halt-on-error dwarf6.tex

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
	-rm -f *.cb
	-rm -f *.cb2
	-rm -f p2.txt
archive:
	sh bldtar.sh

# this is only useful if you ran make all beforehand
check:
	@echo '**********************'
	@echo '*** Cosmetic issues'
	@echo '**********************'
	@egrep '(Under)|(Over)' dwarf6.log || echo "None!"
	@echo '**********************'
	@echo '*** Missing references'
	@echo '**********************'
	@grep 'undef' dwarf6.log || echo "None!"

