
for i in ../latexdoc/*.tex
do
    python charfix.py $i
    mv $i.out $i
done
