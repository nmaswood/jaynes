import os

_f = os.path.dirname

_root = _f(_f(os.path.abspath(__file__)))
ROOT_DIR = os.path.join(_root, 'resources')
DERIVED_DIR = os.path.join(_root, 'derived')
