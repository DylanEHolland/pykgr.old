from pykgr import config


def import_from_string(string):
    # Return an import module from a string
    # e.g. example.class

    packages = string.split(".")
    print(packages)
    potential_module = __import__(string, fromlist=[packages[1]])
    package_class = getattr(potential_module, packages[1])

    return package_class


def load_config(args):
    # Update config class if files are present

    for conf_file in [
        "%s/.pykgr.json" % os.environ.get('HOME'),
        "%s/pykgr.json" % os.environ["PWD"]
    ]:
        if os.path.isfile(conf_file):
            config.from_file(conf_file)