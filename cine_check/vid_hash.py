import os
import hashlib

def generate(dpx, register_file, dpx_files,):
    hash_register = os.path.join(dpx, register_file)

    if os.path.isfile(hash_register):
        print('Hash Register exists in {}'.format(dpx))
    else:
        write = open((hash_register), 'w')
        write.close()

        for x in dpx_files:
            if os.path.isdir(x):
                continue
            else:
                with open(x, 'rb') as f:
                    md5 = hashlib.md5()
                    while buffer := f.read(8192):
                        md5.update(buffer)

                    fn = os.path.basename(x)
                    hash = md5.hexdigest()
                    hash_write = '{} *{}'.format(hash, fn)
                    print('GENERATED: {} hash for {}'.format(hash, fn))

                    with open((hash_register), 'r') as register:
                        if hash in register.read():
                            continue
                        else:
                            with open((hash_register), 'a') as register:
                                register.write(hash_write + '\n')
