import logging
import os
import hashlib
import time
import sys
import globals


def verify(fn, copy_to, dest_register):

    logger = logging.getLogger('__main__.' + __name__)

    verify_file = os.path.join(copy_to, fn)

    tries = 10
    for i in range(tries):
        if os.path.exists(copy_to):
            try:
                with open(dest_register, 'r') as hash_verification:
                    for line in hash_verification:
                        line_name = line[34:].strip()
                        if line_name == fn:
                            line_hash = line[:32]
                            with open(verify_file, 'rb') as f:
                                md5 = hashlib.md5()
                                while buffer := f.read(8192):
                                    md5.update(buffer)
                                    file_hash = md5.hexdigest()

                                if file_hash == line_hash:
                                    logger.info('VERIFIED: {} hash for {}'.format(file_hash, fn,))
                                    globals.globalvar()
                                    globals.hash_verified = True
#                                    return globals.hash_verified

                                else:
                                    logger.warning('FAILED: {} hash does not verify for {}'.format(file_hash, fn))
                                    globals.globalvar()
                                    globals.hash_verified = False
#                                    return globals.hash_verified
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
