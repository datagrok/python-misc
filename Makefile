
default: test

test:
	python -m datagrok.misc.doctest

clean:
	find -name '*.pyc' -delete
