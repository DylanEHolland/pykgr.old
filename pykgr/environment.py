import os
from pykgr import config
from pykgr.builder import Builder
import shutil


class Environment(object):
    builder = None
    variables = None
    
    def __init__(self):
        self.variables = dict(os.environ)
        self.builder = Builder(
            directory=config.builder_directory
        )

    def build_builder(self):
        pass

    def build_package(self, package_name):
        self.builder.build(package_name)

    def destroy(self):
        shutil.rmtree(config.main_directory)

        if not os.path.exists(config.main_directory):
            return True
        return False

    def __str__(self):
        return "<Environment: %s>" % id(self)


def build_directories():
    print("Creating directories", config.main_directory)
    for d in [
        config.main_directory,
        config.source_directory,
        config.source_tarballs_directory,
        config.library_directory
    ]:
        if not os.path.exists(d):
            os.mkdir(d)


def initialize():
    build_directories()
    env = Environment()

    return env 