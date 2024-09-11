#/bin/bash

latex dwarf6.tex
latex dwarf6.tex
makeindex dwarf6
latex dwarf6.tex
latex dwarf6.tex
dvips dwarf6.dvi -o dwarf6.ps
ps2pdf dwarf6.ps dwarf6.pdf
dvi2tty -w150 dwarf6.dvi -o rendered/dwarf6.txt
mv dwarf6.dvi dwarf6.pdf rendered
