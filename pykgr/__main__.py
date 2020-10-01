from argparse import ArgumentParser
from pykgr.builder import Builder
from pykgr import config
import os

def arguments():
    ap = ArgumentParser()
    ap.add_argument("--init", action="store_true")
    ap.add_argument("--package-module", help="Append module folder to package search path")
    ap.add_argument("--package-file", "-p", help="Pass a .py file containing a pykgr class")
    return ap.parse_args()

def initialize(conf):
    os.mkdir(conf.main_directory)
    os.mkdir(conf.source_directory)
    os.mkdir(conf.source_tarballs_directory)

args = arguments()
print("Using:", config)

if not os.path.exists(config.main_directory):
    if args.init:
        initialize(config)
    else:
        print("Please initialize")
        exit(-1)
else:
    pykgr_builder = Builder(
        directory = config.builder_directory
    )

    if args.package_module:
        python_path = os.environ.get('PYTHONPATH')
        if not python_path:
            python_path = ""

        python_path = "%s:%s" % (args.package_module, python_path)
        os.environ['PYTHONPATH'] = python_path

    if args.package_file:
        package_file = args.package_file
        packages = package_file.split(".")
        
        potential_module = __import__(package_file, fromlist=[packages[1]])
        package_class = getattr(potential_module, packages[1])

        pykgr_builder.build(package_class)