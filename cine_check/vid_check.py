import os
import yaml
import tkinter as tk
from tkinter import filedialog
import time
import sys
from vid_hash import generate
from vid_copy import filetrans
from test import test

collection = {}
files = []
missing = []

with open('WA2011.yml', 'r') as read:
    data = yaml.load(read, Loader=yaml.FullLoader)
    collection.update(data)

root = tk.Tk()
root.withdraw()

for key, value in collection.items():
    print(':::::: Insert drive {} ::::::'.format(key))
    print(':::::: Select SOURCE location ::::::')
    time.sleep(2)

    src = filedialog.askdirectory()
    src_dpx = [dir for dir in os.listdir(src)
                if os.path.isdir(os.path.join(src, dir))]

    print(':::::: Please select copy DESTINATION ::::::')
    time.sleep(2)

    dest = filedialog.askdirectory()

    for f in value['files']:
        if f in src_dpx:
            files.append(f)
            print('{} in source'.format(f))
#            dpx = os.path.join(src, f)
#            test(f, dpx)
#            generate(f, dpx)
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
#        test(f, dpx)
        generate(file, dpx)
        filetrans(file, dpx, dest)

    files[:] = []
