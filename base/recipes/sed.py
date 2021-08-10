import pykgr


class Sed(pykgr.Package):
    # Can't call it "file" due to pythons built-in

    file_url = "http://ftp.gnu.org/gnu/sed/sed-4.8.tar.xz"
    file_name = "sed-4.8.tar.xz"
    name = "sed"
    version = "4.8"
    no_build_dir = True

