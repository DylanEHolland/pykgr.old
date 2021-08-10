import pykgr


class Xz(pykgr.Package):
    # Can't call it "file" due to pythons built-in

    file_url = "https://tukaani.org/xz/xz-5.2.5.tar.xz"
    file_name = "xz-5.2.5.tar.xz"
    name = "xz"
    version = "5.2.5"
    no_build_dir = True

