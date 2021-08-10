import pykgr


class Findutils(pykgr.Package):
    # Can't call it "file" due to pythons built-in

    file_url = "http://ftp.gnu.org/gnu/findutils/findutils-4.8.0.tar.xz"
    file_name = "findutils-4.8.0.tar.xz"
    name = "findutils"
    version = "4.8.0"
    no_build_dir = True
