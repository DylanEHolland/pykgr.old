import os

class Configuration:
    prefix = "pykgr_"

    def __init__(self):
        self.root_directory = getenv(self.prefix, "root_directory", envget("HOME"))
        self.main_directory = getenv(self.prefix, "main_directory", "%s/pykgr" % self.root_directory)
        self.builder_directory = getenv(self.prefix, "builder_directory", "%s/builder" % self.main_directory)
        self.source_directory = getenv(self.prefix, "source_directory", "%s/source" % self.main_directory)
        self.package_path = getenv(self.prefix, "package_path", "%s/packages" % self.main_directory)

    def __str__(self):
        return "<pykgr.Configuration %s>" % str(self.all())

    def all(self):
        buffer = {}
        for key in dir(self):
            if "__" not in key and key != "prefix" and not callable(getattr(self, key)):
                buffer[key] = getattr(self, key)

        return buffer

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