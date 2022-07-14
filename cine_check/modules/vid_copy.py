import logging
import os
import time
import shutil
import sys

def filetrans(x, fn, copy_to):

    logger = logging.getLogger('__main__.' + __name__)

    file_check = os.path.join(copy_to, fn)

    tries = 10
    for i in range(tries):
        if os.path.isfile(file_check):
            logger.warning('File {} exists at DESTINATION'.format(fn, copy_to))
            break
        else:
            if os.path.exists(copy_to):
#            time.sleep(1)
                try:
                    shutil.copy2(x, copy_to)
                    if os.path.isfile(file_check):
                        logger.info('COPIED: {} to {}'.format(fn, copy_to))
                        break
                except Exception as e:
                    logger.warning(e)
            else:
                time.sleep(3)
                tries = tries -1
                attempt = i +1
                if attempt == 10:
                    logger.warning('EXIT')
                    sys.exit(0)
                else:
                    logger.warning('RETRYING {} - {} is not accessible'.format(attempt, copy_to))
                    continue
