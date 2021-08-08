import os


def get_current_path():
    path = os.environ['PWD']
    split_path = path.split("/")
    if split_path[-1] == "tests":
        path = "/".join(split_path[:-1])
    return path
