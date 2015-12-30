#
# Makefile for bowl_pool
# John R. Dowdle
# Dec 30 2014
#
#
#

all:	
	python main.py
	rst2html srv/index.txt > srv/index.html
	cp -r srv/* ~/code/jrd.spinodal.org/jorodo.github.io/bowl_pool/

test:	
	python main.py -d srv/test
	rst2html srv/test/index.txt > srv/test/index.html
	cp -r srv/test/* ~/code/jrd.spinodal.org/jorodo.github.io/bowl_pool/test/

clean:
	rm srv/*.*
	rm -rf srv/test/*

clobber:
	rm *.pyc srv/*
	rm -rf srv/*

