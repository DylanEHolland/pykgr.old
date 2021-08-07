def import_from_string(string):
    # Return an import module from a string
    # e.g. example.class

    packages = string.split(".")
    print(packages)
    potential_module = __import__(string, fromlist=[packages[1]])
    package_class = getattr(potential_module, packages[1])

    return package_class