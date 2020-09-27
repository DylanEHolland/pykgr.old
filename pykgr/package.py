from pykgr.shell import Shell
import pykgr

class Package(object):
    name = None
    shell = None
    version = None

    def __build__(self):
        self.fetch()
        self.prepare()
        self.make()
        self.install()

    def __init__(self, **kwargs):
        self.shell = Shell(PWD=pykgr.config.source_directory)

    def __str__(self):
        return "<package [%s-%s]>" % (self.name, str(self.version))

    def fetch(self):
        pass

    def install(self):
        pass

    def make(self):
        pass

    def prepare(self):
        pass