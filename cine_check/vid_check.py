import os
import logging
from datetime import datetime
import yaml
import tkinter as tk
from tkinter import filedialog
import time
import glob
import sys
from alive_progress import alive_bar
import shutil
from modules.vid_hash import generate
from modules.vid_copy import filetrans
from modules.vid_verify import verify
import globals


logTS = datetime.now().strftime('%Y%m%d_%H.%M__log.log')
logloc = os.getcwd()
log = '{}/logs/{}'.format(logloc, logTS)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(module)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler(log)

file_handler.setFormatter(formatter)
#stream_handler = logging.StreamHandler()

logger.addHandler(file_handler)
#logger.addHandler(stream_handler)

collection = {}
files = []
missing = []

yamloc = os.getcwd()
drivedata = '{}/data/WA2011.yml'.format(yamloc)

with open(drivedata, 'r') as read:
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

    logger.info('SOURCE: {}'.format(src))
    logger.info('DESTINATION: {}'.format(dest))

    for f in value['files']:
        if f in src_dpx:
            files.append(f)
            print('{} in source'.format(f))
        else:
            missing.append(f)

    if not len(missing) == 0:
        print('{} not in source'.format(missing))
        logger.warning('{} not in source'.format(missing))
        print('Would you like to continue?')
        print('Press q to quit or any other key to continue')
        quit = input()
        if quit == 'q':
            sys.exit(0)

    missing[:] = []
    

    for file in files:
#        print('--------{}--------'.format(file))

        dpx = os.path.join(src, file)
        dpx_files = sorted(glob.glob(dpx + '/*.dpx', recursive=True))
#        print(dpx_files)

        register_file = '{}_dpx_hash_register.md5'.format(file)
        src_register = os.path.join(dpx, register_file)
        dest_register = os.path.join(dest, file, register_file)
        safe_copy = '_complete'
        safe_copy_loc = os.path.join(dpx, safe_copy)
        fail_copy = '_failed'
        fail_copy_loc = os.path.join(dpx, fail_copy)

        copy_to = os.path.join(dest, file)

        tries = 10
        for i in range(tries):
            if os.path.exists(dest):
                try:
                    if not os.path.exists(copy_to):
                        os.mkdir(copy_to)
                    else:
                        print('{} exists at DESTINATION'.format(file, dest))

                    if os.path.isfile(dest_register):
                        print('Hash Register exists at DESTINATION'.format(file))
                    else:
                        write = open((dest_register), 'w')
                        write.close()

                    if len(dpx_files) == 0:
                        logger.warning('SKIPPING {} no dpx files found'.format(file))
                    else:
                        if os.path.isfile(src_register):
                            print('Hash Register exists at SOURCE')
                        else:
                            write = open((src_register), 'w')
                            write.close()
                        if os.path.exists(safe_copy_loc):
                            print('/_complete safe copy location exists')
                        else:
                            os.mkdir(safe_copy_loc)
                    break
                except Exception as e:
                    logger.warning(e)

            else:
                time.sleep(3)
                tries = tries -1
                attempt = i +1
                if attempt == 10:
                    print('Attempts to contact {} exceeded'.format(dest))
                    logger.warning('Attempts to contact {} exceeded'.format(dest))
                    print('EXIT')
                    logger.warning('EXIT')
                    sys.exit(0)
                else:
                    print('RETRYING {} {} is not accessible'.format(attempt, dest))
                    logger.warning('RETRYING {} {} is not accessible'.format(attempt, dest))
                    continue

        with alive_bar(len(dpx_files), title=f'{file}') as bar:
            for x in dpx_files:
                if os.path.isdir(x):
                    continue
                else:
                    fn = os.path.basename(x)
                    copied_file = os.path.join(copy_to, fn)
                    generate(x, fn, src_register, dest_register)
                    filetrans(x, fn, copy_to)
                    verify(fn, copy_to, dest_register)
    #                test()

                    try:
                        if os.path.isfile(copied_file) and globals.hash_verified == True:
                            shutil.move(x, safe_copy_loc)
                            print('SUCCESS: {}'.format(fn))
                            logger.debug('SUCCESS: {}'.format(fn))
                        elif os.path.isfile(copied_file) or globals.hash_verfied == False:
                            if os.path.exists(fail_copy_loc):
                                shutil.move(copied_file, fail_copy_loc)
                                logger.warning('FAILED: {}'.format(fn))
                            else:
                                os.mkdir(fail_copy_loc)
                                shutil.move(copied_file, fail_copy_loc)
                                print('FAILED: {}'.format(fn))
                                logger.warning('FAILED: {}'.format(fn))

                    except Exception as e:
                        print(e)
                        logger.warning(e)
                
                time.sleep(0.01)
                bar() 

    files[:] = []
