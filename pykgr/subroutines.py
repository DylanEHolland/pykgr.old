import pykgr
import sys
import os


def add_module(mod_path):
    # mod_path = "/".join(mod_path.split("/")[:-1])
    if mod_path not in sys.path:
        sys.path.insert(0, mod_path)


def import_from_string(string):
    # Return an import module from a string
    # e.g. example.class

    packages = string.split(".")
    if len(packages):
        main_package = ".".join(packages[0:-1])
        main_class = packages[-1]
        potential_module = __import__(main_package, fromlist=[main_class])
        package_class = getattr(potential_module, main_class)

        return package_class


def load_config(args):
    # Update config class if files are present

    for conf_file in [
        "%s/.pykgr.json" % os.environ.get('HOME'),
        "%s/pykgr.json" % os.environ["PWD"]
    ]:
        if os.path.isfile(conf_file):
            pykgr.config.from_file(conf_file)

    pykgr.config.setup(
        main_dir=pykgr.config.main_directory
    )

    if args.verbose:
        pykgr.config.verbose = args.verbose


def replace_vars(instance, text):
    for key in instance.keys():
        string_to_find = "{%s}" % key
        if string_to_find in text:
            value = object.__getattribute__(instance, key)
            text = text.replace(
                string_to_find,
                value
            )

    return text


def setup_paths(args):
    # Setup pythonpath so we can call local package
    # classes.

    if pykgr.config.toolchain_package_module:
        add_module(pykgr.config.toolchain_package_module)

    if args.package_module:
        packages = args.package_module
        for pm in packages:
            add_module(pm)

    print("\n=\nFinal $PYTHONPATH:")
    for d in sys.path:
        if len(d):
            print("\t%s" % d)
    print("==\n")