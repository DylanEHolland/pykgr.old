from pykgr.shell import Command, Shell

#sh = Shell()
def test_command():
    cmd = Command("hello")
    output = "Hello, world!"
    
    assert cmd.run() == 'Hello, world!\n'