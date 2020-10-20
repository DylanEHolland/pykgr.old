from pykgr import config

from argparse import ArgumentParser
from pykgr.builder import Builder
from pykgr.environment import initialize
from pykgr import config
import os

def arguments():
    ap = ArgumentParser()
    ap.add_argument("--init", action="store_true")
    # ap.add_argument("--package-module", "-pm", help="Append module folder to package search path")
    # ap.add_argument("--package-file", "-p", help="Pass a .py file containing a pykgr class")
    
    return ap.parse_args()

def load_config(args):
    for conf_file in [
        "%s/.pykgr.json" % os.environ.get('HOME'),
        "%s/pykgr.json" % os.environ["PWD"]
    ]:
        if os.path.isfile(conf_file):
            config.from_file(conf_file)

def setup_paths(args):
    python_path = os.environ.get('PYTHONPATH')
    if not python_path:
        python_path = ""

    python_path = "%s:%s" % (args.package_module, python_path)
    if config.local_package_module:
        python_path = "%s:%s" % ("%s:%s" % (args.package_module, python_path), python_path)

    os.environ['PYTHONPATH'] = python_path

def spawn_interface():
    args = arguments()
    load_config(args)

    if args.init:
        print("Initializing")
        initialize(config)