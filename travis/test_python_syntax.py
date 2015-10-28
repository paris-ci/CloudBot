__author__ = 'arthur'
import fnmatch
import os
import sys

error = False
print("Travis: Testing all PY files in source")

for root, dirs, files in os.walk('.'):
    for filename in fnmatch.filter(files, '*.py'):
        try:
            file = os.path.join(root, filename)
            source = open(file, 'r').read() + '\n'
            compile(source, file, 'exec')
            print("Travis: {} is a valid PY file".format(filename))
        except Exception as e:
            error = True
            print("Travis: {} is not a valid PY file, load threw exception:\n{}".format(filename, e))

if error:
    sys.exit(1)
