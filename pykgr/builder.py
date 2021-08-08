import os
from pykgr.subroutines import import_from_string


class Builder(object):
    data = None

    def __init__(self, **kwargs):
        self.data = BuilderData(**kwargs)

        if not self.data.directory:
            raise Exception("What can we do without a directory?")

        if not os.path.exists(self.data.directory):
            os.mkdir(self.data.directory)

    def build(self, package_class):
        if type(package_class) == str:
            package_class = import_from_string(package_class)

        package_to_build = package_class()
        package_to_build.__build__()

    def build_toolchain(self):
        binutils = import_from_string("base.toolchain.binutils.Binutils")
        #gcc = import_from_string("toolchain.Gcc")

        self.build(binutils)
        #self.build(gcc)

    def build_library(self):
        lib = import_from_string("toolchain.glibc")
        self.build(lib)


class BuilderData:
    def __init__(self, **kwargs):
        self.directory = None

        self_keys = [row for row in dir(self) if "__" not in row and not callable(getattr(self, row))]
        for key in kwargs:
            if key in self_keys:
                setattr(self, key, kwargs.get(key))


class BuilderLibrary:
    # For maintaining a local glibc
    pass