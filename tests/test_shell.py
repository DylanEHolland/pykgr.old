from pykgr.shell import Command, Shell


def test_command():
    cmd = Command("hello")
    output = "Hello, world!"

    assert cmd.run() == 'Hello, world!\n'


def test_command_methods():
    sh = Shell()
    ls_command = sh.command("ls", "/").run()

    assert ls_command == sh.ls("/")


def test_shell_compile():
    # Compile a fresh binutils
    src_url = "http://ftp.gnu.org/gnu/binutils/binutils-2.35.tar.xz"
    sh = Shell
    print(sh)

    sh = sh()
    print(sh)

    sh = Shell(PWD="/tmp")
    sh.command(
        "wget", 
        "-c", 
        src_url
    ).run(
        display_output = True
    )
    
    sh.command("tar", "xvf", "binutils-2.35.tar.xz").run()
    sh.cd("binutils-2.35")
    sh.command("mkdir", "-pv", "build").run(display_output=True)
    sh.cd("/tmp/binutils-2.35/build")
    sh.command(
        "../configure",
        "-prefix=/tmp/not-useable-binutils"
    ).run(display_output = True)
    sh.command(
        "make", "-j12"
    ).run(display_output = True)
    sh.command(
        "make", "-j12", "install"
    ).run(display_output = True)


if __name__ == "__main__":
    test_command()
    test_command_methods()
    test_shell_compile()