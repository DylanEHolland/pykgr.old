import pykgr
import os


class Glibc(pykgr.Package):
    file_url = "http://ftp.gnu.org/gnu/glibc/glibc-2.32.tar.xz"
    file_name = "glibc-2.32.tar.xz"
    name = "glibc"
    version = "2.32"
