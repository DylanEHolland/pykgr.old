from pykgr.subroutines import load_config, setup_paths
from argparse import ArgumentParser
from pykgr.environment import Environment, initialize
from pykgr import config
import os


def arguments():
    ap = ArgumentParser()
    
    ap.add_argument("--build-library", action="store_true")
    ap.add_argument("--build-toolchain", action="store_true")
    ap.add_argument("--init", action="store_true")
    ap.add_argument("--package-file", "-p", help="Pass a package class to be built and installed")
    ap.add_argument("--package-module", "-pm", action="append")
    
    return ap.parse_args()


def spawn_interface():
    # Handle command line arguments

    args = arguments()
    load_config(args)
    setup_paths(args)

    if args.init:
        print("Initializing")
        env = initialize()
    else:
        env = Environment()

    if config.toolchain_package_module:
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
        if not os.path.exists("%s/lib" % config.library_directory):
            print("Building glibc")
            env.builder.build_library()
    
    if args.build_library:
        print("Building glibc")
        env.builder.build_library()

    if args.package_file:
        print("Building", args.package_file)
        env.build_package(args.package_file)
