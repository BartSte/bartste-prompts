from os.path import abspath, dirname, join, normpath

root: str = normpath(abspath(join(dirname(__file__))))
instructions: str = join(root, "_instructions")
