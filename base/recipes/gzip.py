import pykgr


class Gzip(pykgr.Package):
    # Can't call it "file" due to pythons built-in

    file_url = "http://ftp.gnu.org/gnu/gzip/gzip-1.10.tar.xz"
    file_name = "gzip-1.10.tar.xz"
    name = "gzip"
    version = "1.10"
    no_build_dir = True

