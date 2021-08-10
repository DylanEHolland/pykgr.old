import pykgr


class FileTool(pykgr.Package):
    # Can't call it "file" due to pythons built-in

    file_url = "http://ftp.astron.com/pub/file/file-5.39.tar.gz"
    file_name = "file-5.39.tar.gz"
    name = "file"
    version = "5.39"
    no_build_dir = True
