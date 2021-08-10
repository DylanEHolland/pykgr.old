import pykgr


class Patch(pykgr.Package):
    # Can't call it "file" due to pythons built-in

    file_url = "http://ftp.gnu.org/gnu/patch/patch-2.7.6.tar.xz"
    file_name = "patch-2.7.6.tar.xz"
    name = "patch"
    version = "2.7.6"
    no_build_dir = True

