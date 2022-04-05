import os
import time
import shutil

def filetrans(file, dpx, dest):
    copy_to = os.path.join(dest, file)
    tries = 10
    for i in range(tries):
        if os.path.exists(dest) == True:
#            print('{} exists'.format(dest))
#            time.sleep(1)
            try:
                os.mkdir(copy_to)
                shutil.copytree(dpx, copy_to, dirs_exist_ok=True)
                print('COPIED: from {} to {}'.format(dpx, dest))
                break
            except Exception as e:
                print(e)
        else:
            time.sleep(3)
            tries = tries -1
            attempt = i +1
            print('RETRYING {} - {} not accessible'.format(dest, attempt) )
            continue
