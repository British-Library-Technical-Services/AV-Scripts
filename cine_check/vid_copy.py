import os
import shutil

def filetrans(file, dpx, dest):
    copy_to = os.path.join(dest, file)
    os.mkdir(copy_to)
    print('COPYING: {} to {}'.format(file, dest))
    shutil.copytree(dpx, copy_to, dirs_exist_ok=True)
