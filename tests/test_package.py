import pykgr
import os
pykgr.config.setup("/tmp/pykgr_test")


class Hello(pykgr.Package):
    file_url = "https://ftp.gnu.org/gnu/hello/hello-2.9.tar.gz"
    file_name = "hello-2.9.tar.gz"
    name = "hello"
    version = "2.9"


class Vim(pykgr.Package):
    file_url = "https://github.com/vim/vim/archive/refs/tags/v8.2.3301.tar.gz"
    file_name = "v8.2.3301.tar.gz"
    name = "vim"
    version = "8.2.3301"
    compile_directory = "/src"
    no_build_dir=True

    def pre_configure_run(self):
        # Already should be in `working_dir`
        self.shell.make("distclean", display_output=True)


def test_build():
    env = pykgr.Environment()

    env.build_package(Hello)
    assert os.path.exists(pykgr.config.packages_directory+"/bin/hello") is True

    env.build_package(Vim)
    assert os.path.exists(pykgr.config.packages_directory+"/bin/vim") is True


if __name__ == "__main__":
    test_build()
