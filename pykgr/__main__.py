from argparse import ArgumentParser
from pykgr.builder import Builder
from pykgr import config
import os
from pykgr import cli

args = cli.arguments(ArgumentParser())

conf_file = "%s/.pykgr.json" % os.environ.get('HOME')
if os.path.isfile(conf_file):
    config.from_file(conf_file)

print("Using:", config)
if not os.path.exists(config.main_directory):
    if args.init:
        cli.initialize(config)
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
        if config.local_package_module:
            python_path = "%s:%s" % ("%s:%s" % (args.package_module, python_path), python_path)

        os.environ['PYTHONPATH'] = python_path

    if args.package_file:
        package_file = args.package_file
        packages = package_file.split(".")
        
        potential_module = __import__(package_file, fromlist=[packages[1]])
        package_class = getattr(potential_module, packages[1])

        pykgr_builder.build(package_class)
        