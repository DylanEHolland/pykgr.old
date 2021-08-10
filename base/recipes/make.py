import pykgr


class Make(pykgr.Package):
    # Can't call it "file" due to pythons built-in

    file_url = "http://ftp.gnu.org/gnu/make/make-4.3.tar.gz"
    file_name = "make-4.3.tar.gz"
    name = "make"
    version = "4.3"
    no_build_dir = True

