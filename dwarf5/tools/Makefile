# Makefile which tests the python internals for sanity.

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
	python refclassfixup.py test2.in.out
	# checking for idempotence
	diff test2.in.out test2.in.out.out
