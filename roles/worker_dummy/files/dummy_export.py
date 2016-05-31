import os
from shutil import copyfile

input_dir = '/data/input'
output_dir = '/data/output'

for root, dirs, files in os.walk(input_dir):
    for f in files:
        name, ext = os.path.splitext(f)
        if ext == '.ini':
            copyfile(os.path.join(root, f), os.path.join(output_dir, "-".join(['export', f])))
