import pykgr


class Tar(pykgr.Package):
    # Can't call it "file" due to pythons built-in

    file_url = "http://ftp.gnu.org/gnu/tar/tar-1.34.tar.xz"
    file_name = "tar-1.34.tar.xz"
    name = "tar"
    version = "1.34"
    no_build_dir = True

