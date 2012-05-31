# Makefile which tests the python internals for sanity.

all:
	echo 'make clean' and 'make test' do something.
	echo default does nothing
clean:
	-rm -f *.pyc
	-rm -f *.tmp
	-rm -f *.out
	
test:	
	python printtokens.py test1.in >test1.tmp
	diff test1.tmp test1.base
	python copyfile.py test1.in 
	diff test1.in test1.in.out
	python refclassfixup.py test2.in
	diff test2.in.out test2.base
	# checking for idempotence
	python refclassfixup.py test2.in.out
	diff test2.in.out test2.in.out.out
	python taglink.py test1.in
	diff test1.in.out taglink.base
	# checking for idempotence
	python taglink.py test1.in.out
	diff test1.in.out.out taglink.base
	python printstandard.py printstandard.in >printstandard.out
	diff printstandard.out printstandard.base
	python tohyphen.py tohyphen.in
	diff tohyphen.in.out tohyphen.base
	# checking for idempotence
	python tohyphen.py tohyphen.in.out
	diff tohyphen.in.out.out tohyphen.base
	python attrlink.py attrlink.in
	diff attrlink.in.out attrlink.base
	# checking for idempotence
	python attrlink.py attrlink.in.out
	diff attrlink.in.out.out attrlink.base
	python formlink.py formlink.in
	diff formlink.in.out formlink.base
	python formlink.py formlink.in.out
	diff formlink.in.out.out formlink.base
     
