# pykgr

## A simple, user focused, build system (for learning purposes)

You will want to edit the pykgr.json file in the root of this repo to point to the
repos location.  Alternatively you can setup a .pykgr.json and pip install it (but
use any other dir as the one in this directory will overwrite certain configurations.)

Then just `python -m pykgr --init -p packages.python`

The packages module is located in the `base` directory which is imported by default.
You can pass any arbitrary directory with submodules to then use, e.g. this 
directory

    . mypackages
        . recipes
            . hello.py
            . python.py

would allow you to install vim like so

`python -m pykgr --init --build-toolchain -p mypackages.recipes.hello.Hello`

It can also be used in code, like this

```
import pykgr

class Hello(pykgr.Package):
    file_url = "https://ftp.gnu.org/gnu/hello/hello-2.9.tar.gz"
    file_name = "hello-2.9.tar.gz"
    name = "hello"
    version = "2.9"
    
env = pykgr.Environment()
env.build_package(Hello)
```

Which will build the package.  The goal is to allow people to maintain a git repo
similar to mypackages, that they could then pull from and build a root-free system
of packages that, by default, install to $HOME/pykgr.