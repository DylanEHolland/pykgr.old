import pykgr


class Gawk(pykgr.Package):
    # Can't call it "file" due to pythons built-in

    file_url = "http://ftp.gnu.org/gnu/gawk/gawk-5.1.0.tar.xz"
    file_name = "gawk-5.1.0.tar.xz"
    name = "gawk"
    version = "5.1.0"
    no_build_dir = True
