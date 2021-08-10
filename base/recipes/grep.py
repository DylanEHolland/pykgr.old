import pykgr


class Grep(pykgr.Package):
    # Can't call it "file" due to pythons built-in

    file_url = "http://ftp.gnu.org/gnu/grep/grep-3.6.tar.xz"
    file_name = "grep-3.6.tar.xz"
    name = "grep"
    version = "3.6"
    no_build_dir = True
