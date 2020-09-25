import os
import subprocess

class Shell(object):
    # A pythonic shell

    def __new__(cls, *args, **kwargs):
        # `args` are treated as arguments into a shell,
        # e.g. `Shell("ls -l")` or `Shell("ls", "-l")` 
        # returns the stdout of `/bin/sh -c "ls -l"` 
        # while `Shell("ls")` returns a "program" (below.)  
        #
        # Kwargs are environment variables, e.g.
        # Shell("echo $test", test="world") is akin
        # to test="world".
        #
        # An empty class returns a blank shell instance,
        # for "interactive" mode like `sh = Shell(); sh.command("ls -l")`
        # 
        # For a blank shell in a given folder you would, e.g.
        # Shell(PWD="/my/source/code/folder").command("configure -flag")
        pass

class Command:
    args = None
    program = None

    def __init__(self, command, *args, **kwargs):
        self.program = command
        self.args = args
    
    def run(self):
        command_line = [self.program] + list(self.args)
        out = subprocess.Popen(
            command_line, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT
        )

        
        output, error = out.communicate()
        return output