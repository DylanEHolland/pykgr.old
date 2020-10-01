import os
import json

class Configuration:
    prefix = "pykgr_"

    def __init__(self):
        self.root_directory = getenv(self.prefix, "root_directory", envget("HOME"))
        self.main_directory = getenv(self.prefix, "main_directory", "%s/pykgr" % self.root_directory)
        self.builder_directory = getenv(self.prefix, "builder_directory", "%s/builder" % self.main_directory)
        self.source_directory = getenv(self.prefix, "source_directory", "%s/source" % self.main_directory)
        self.source_tarballs_directory = getenv(self.prefix, "source_tarballs_directory", "%s/tarballs" % self.source_directory)
        self.package_path = getenv(self.prefix, "package_path", "%s/packages" % self.main_directory)
        self.make_opts = getenv(self.prefix, "make_opts", "12")

    def __str__(self):
        return "<pykgr.Configuration %s>" % str(self.all())

    def all(self):
        buffer = {}
        for key in self.keys():
            buffer[key] = getattr(self, key)

        return buffer

    def keys(self):
        return [
            key
            for key in dir(self)
            if "__" not in key and key != "prefix" and not callable(getattr(self, key))
        ]

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
                    setattr(self, k, conf[k])

def envget(key):
    return os.environ.get(key)

def getenv(prefix, key, default_value = None):
    key_name = "%s%s" % (
        prefix,
        key
    )
    
    value = envget(key_name)
    if not value:
        value = default_value
    return value

conf = Configuration()