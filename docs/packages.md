# Packages

## Package Class

```
class Package:
    build_directory = None
    code_directory = None
    compile_directory = None # e.g. if code_directory has a subdir, so "{code_directory}/src" for vim
    subdirectory_location = None
    file_name = None
    file_url = None
    name = None
    repo = False
    repo_url = None
    shell = None
    version = None
    no_build_dir = False

    __build__(self)

    __init__(self, **kwargs)

    __initialize__(self)

    configure(self)

    decompress(self)

    fetch(self)

    generate(self)

    get_code(self)

    install(self)

    make(self)

    prepare(self)

    pre_configure_run(self)

    untar(self)
```