PY_INT=python3

all: setup

clean:
	@-for d in `find pykgr example -name __pycache__`; do rm -rv $$d; done;
	@-if [ -d dist ]; then rm -r dist; fi;
	@-if [ -f MANIFEST ]; then rm MANIFEST; fi;

prepare: setup
	@-$(PY_INT) setup.py sdist;

proper: clean
	@-if [ -d env ]; then rm -r env; fi;

push:
	@-twine upload dist/*;

setup:
	@-if ! [ -d env ]; then $(PY_INT) -m venv env; fi;
	@-source env/bin/activate && pip install -r requirements.txt;
