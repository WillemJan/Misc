.PHONY: clean test pony doc

init:
	bash ./init.sh

clean:
	echo "Cleaning"
	find . -name '*~' -exec rm -f {} +
	find . -type f -name '*.pyc' -exec rm {} +
	find . -type f -name '*.pyo' -exec rm {} +
	find . -type d -name 'build' -exec rm -rf {} +
	find . -type d -name 'dist' -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	find . -name 'PyZ3950_parsetab.py' -type f -exec rm {} +

install:
	python ./setup.py install

test:
	python ./run-tests.py

all: 	
	clean test

pony:
	find . -name '__init__.py' -exec cat {} +

doc:
	sh ./gen_doc.sh
