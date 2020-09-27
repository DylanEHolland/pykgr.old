import pykgr

class binutils(pykgr.Package):
    file_url = "http://ftp.gnu.org/gnu/binutils/binutils-2.35.tar.xz"
    name = "binutils"
    version = "2.35"

    def fetch(self):
        self.shell.cd(pykgr.config.source_tarballs_directory)
        print(self.shell.PWD)
        #print(self.shell.PWD, self.shell.ls())
        
