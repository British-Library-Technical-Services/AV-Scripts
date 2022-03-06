import os
import glob
import hashlib

def generate(file, dpx):
    print(f'--------{file}----------')
    dpx_files = glob.glob(dpx + '/**/*.dpx', recursive=True)

    if len(dpx_files) == 0:
        print(f'No dpx files found in {dpx}')
    
    else:
        register = file + '_dpx_hashes.md5'
        hash_register = os.path.join(dpx, register)

        if os.path.isfile(hash_register):
            print(f'Hash Register exists in {dpx}')
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
                        hash = md5.hexdigest() + ' *' + fn
                        print(hash)
                        with open((hash_register), 'r') as register:
                            if hash in register.read():
                                continue
                            else:
                                with open((hash_register), 'a') as register:
                                    register.write(hash + '\n')
