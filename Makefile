
default: test

test:
	python -m doctest datagrok/*/*.py

clean:
	find -name '*.pyc' -delete
