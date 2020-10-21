from pykgr import config

from argparse import ArgumentParser
from pykgr.builder import Builder
from pykgr.environment import Environment, initialize
from pykgr import config

import os
import sys

def add_module(mod_path):
    mod_path = "/".join(mod_path.split("/")[0:-1])
    if mod_path not in sys.path:
        sys.path.insert(0, mod_path)  

def arguments():
    ap = ArgumentParser()
    
    ap.add_argument("--build-toolchain", action="store_true")
    ap.add_argument("--init", action="store_true")
    ap.add_argument("--package_module", "-pm", action="append")
    
    # ap.add_argument("--package-file", "-p", help="Pass a .py file containing a pykgr class")
    
    return ap.parse_args()

def import_from_string(string):
    # e.g. example.class

    packages = string.split(".")
    potential_module = __import__(string, fromlist=[packages[1]])
    package_class = getattr(potential_module, packages[1])
    
    return package_class

def load_config(args):
    for conf_file in [
        "%s/.pykgr.json" % os.environ.get('HOME'),
        "%s/pykgr.json" % os.environ["PWD"]
    ]:
        if os.path.isfile(conf_file):
            config.from_file(conf_file)

def setup_paths(args):
    # Setup pythonpath so we can call local package
    # classes.

    if config.toolchain_package_module:
        add_module(config.toolchain_package_module)
        add_module(config.toolchain_package_module)

    if args.package_module:
        packages = args.package_module
        for pm in packages:
            add_module(pm)

    print("\n=\nFinal $PYTHONPATH:")
    for d in sys.path:
        if len(d):
            print("\t%s" % d)
    print("==\n")

def spawn_interface():
    args = arguments()
    load_config(args)
    setup_paths(args)

    if args.init:
        print("Initializing")
        env = initialize()
    else:
        env = Environment()

    print("Using toolchain module from", config.toolchain_package_module)
    compiler = "%s/bin/gcc" % config.builder_directory
    
    print("Looking for environment in %s..." % config.main_directory, end=' ')
    if not os.path.isfile(compiler):
        print("\nToolchain doesn't exist!")
    else:
        print("Found!")

    if args.build_toolchain:
        print("Building compiler")
        env.builder.build_toolchain()
    else:
        pass
        #print()