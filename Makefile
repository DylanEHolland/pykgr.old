PY_INT=python3

all: setup

clean:
	@-for d in `find pykgr example base -name __pycache__`; do rm -rv $$d; done;
	@-for d in `find pykgr example base -name *.pyc`; do rm -rv $$d; done;
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

view_links: view_ld_list view_c_list view_cpp_list
	@-echo done;

view_ld_list:
	ld --verbose | grep SEARCH_DIR | tr -s ' ;' \\012;

view_c_list:
	echo | gcc -x c -E -Wp,-v - >/dev/null;

view_cpp_list:
	gcc -x c++ -E -Wp,-v - >/dev/null;