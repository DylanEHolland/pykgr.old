import os
import json

class Configuration(object):
    prefix = "pykgr_"

    def __init__(self):
        self.setup()

    def __str__(self):
        return "<pykgr.Configuration %s>" % str(self.all())

    def all(self):
        buffer = {}
        for key in self.keys():
            buffer[key] = getattr(self, key)

        return buffer

    def from_file(self, json_file):
        print("Loading Config", json_file)
        conf = None
        with open(json_file, 'r') as fp:
            conf = json.loads(fp.read())
            fp.close()

        if conf:
            keys = self.keys()
            for k in conf:
                if k in keys:
                    value = conf[k]
                    if "{" in value:
                        value = replace_vars(self, value)
                    setattr(self, k, value)

    def keys(self):
        return [
            key
            for key in dir(self)
            if "__" not in key and key != "prefix" and not callable(getattr(self, key))
        ]

    def setup(self, root_dir=None):
        self.root_directory = root_dir if root_dir else getenv(self.prefix, "root_directory", envget("HOME"))
        self.main_directory = getenv(self.prefix, "main_directory", "%s/pykgr" % self.root_directory)
        
        self.builder_directory = getenv(self.prefix, "builder_directory", "%s/builder" % self.main_directory)
        self.library_directory = getenv(self.prefix, "library_directory", "%s/library" % self.main_directory)
        self.packages_directory = getenv(self.prefix, "packages_directory", "%s/packages" % self.main_directory)
        
        self.source_directory = getenv(self.prefix, "source_directory", "%s/source" % self.main_directory)
        self.source_tarballs_directory = getenv(self.prefix, "source_tarballs_directory", "%s/tarballs" % self.source_directory)

        self.toolchain_package_module = getenv(self.prefix, "toolchain_package_module", None)
        self.main_package_module = getenv(self.prefix, "main_package_module", "%s/packages" % self.main_directory)
        self.local_package_module = getenv(self.prefix, "local_package_module", None)

        self.make_opts = getenv(self.prefix, "make_opts", "1")
        self.verbose = getenv(self.prefix, "verbose", False)


def envget(key):
    value = os.environ.get(key)
    if value:
        if value.strip() == "True":
            value = True
        elif value.strip() == "False":
            value = False
    return value


def getenv(prefix, key, default_value = None):
    key_name = "%s%s" % (
        prefix,
        key
    )
    
    value = envget(key_name)
    if not value:
        value = default_value
    return value


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


conf = Configuration()