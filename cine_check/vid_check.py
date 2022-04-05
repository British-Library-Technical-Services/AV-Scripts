import os
import yaml
import tkinter as tk
from tkinter import filedialog
import time
import glob
import sys
from vid_hash import generate
from vid_copy import filetrans
from vid_verify import verify
from test import test

collection = {}
files = []
missing = []

with open('WA2011.yml', 'r') as read:
    data = yaml.load(read, Loader=yaml.FullLoader)
    collection.update(data)

root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)

for key, value in collection.items():
    print(':::::: Insert drive {} ::::::'.format(key))
    print(':::::: Select SOURCE location ::::::')
    time.sleep(1)

    src = filedialog.askdirectory()
    src_dpx = [dir for dir in os.listdir(src)
                if os.path.isdir(os.path.join(src, dir))]

    print(':::::: Please select copy DESTINATION ::::::')
    time.sleep(1)

    dest = filedialog.askdirectory()

    for f in value['files']:
        if f in src_dpx:
            files.append(f)
            print('{} in source'.format(f))
        else:
            missing.append(f)

    if not len(missing) == 0:
        print('{} not in source'.format(missing))
        print('Would you like to continue?')
        print('Press q to quit or any other key to continue')
        quit = input()
        if quit == 'q':
            sys.exit(0)

    missing[:] = []

    for file in files:
        dpx = os.path.join(src, file)
        print('--------{}----------'.format(file))
        dpx_files = glob.glob(dpx + '/**/*.dpx', recursive=True)

        register_file = '{}_dpx_hashes.md5'.format(file)
        copied_register = os.path.join(dest, file, register_file)

        if len(dpx_files) == 0:
            print('SKIPPING {} - no dpx files found {}'.format(file, dpx))
            continue
        else:
            generate(dpx, register_file, dpx_files)
            filetrans(file, dpx, dest)
            verify(dest, file, copied_register)

    files[:] = []
