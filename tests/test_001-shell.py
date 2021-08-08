from pykgr.shell import Command, Shell


def test_command():
    cmd = Command("hello")
    output = "Hello, world!"

    assert cmd.run() == 'Hello, world!\n'


def test_command_methods():
    sh = Shell()
    ls_command = sh.command("ls", "/").run()

    assert ls_command == sh.ls("/")


if __name__ == "__main__":
    test_command()
    test_command_methods()