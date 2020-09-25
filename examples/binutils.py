import pykgr

class binutils(pykgr.Package):

    def build(self):
        self.shell.make()

    def fetch(self):
        pass

    def install(self):
        self.shell.make()

    def prebuild(self):
        self.shell(
            "./configure",
            "--disable-nls",
            "--etc"
        )