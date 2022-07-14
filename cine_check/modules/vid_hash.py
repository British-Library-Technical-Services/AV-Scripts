import logging
import os
import hashlib

def generate(x, fn, src_register, dest_register):

    logger = logging.getLogger('__main__.' + __name__)

    with open(x, 'rb') as f:
        md5 = hashlib.md5()
        while buffer := f.read(8192):
            md5.update(buffer)

        hash = md5.hexdigest()
        hash_write = '{} *{}'.format(hash, fn)

    with open((src_register), 'r') as register:
        if hash_write in register.read():
            logger.info('MD5 hash for {} EXISTS in SOURCE register'.format(fn))
        else:
            with open((src_register), 'a') as register:
                register.write(hash_write + '\n')
                logger.info('GENERATED: {} hash for {}'.format(hash, fn))

    with open((dest_register), 'r') as register:
        if hash_write in register.read():
            logger.info('MD5 hash for {} EXISTS in DESTINATION register'.format(fn))
        else:
            with open((dest_register), 'a') as register:
                register.write(hash_write + '\n')
