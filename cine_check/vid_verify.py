import os
import glob
import hashlib


def verify(dest, file):

    register = '{}_dpx_hashes.md5'.format(file)

    dest_loc = os.path.join(dest, file)
    ver_register = os.path.join(dest_loc, register)

    verify_files = glob.glob(dest_loc + '/**/*.dpx', recursive=True)

    for ver in verify_files:
        fn = os.path.basename(ver)
        with open(ver_register, 'r') as hash_verification:
            for line in hash_verification:
                line_name = line[34:].strip()
                if line_name == fn:
                    line_hash = line[:32]
                    with open(ver, 'rb') as f:
                        md5 = hashlib.md5()
                        while buffer := f.read(8192):
                            md5.update(buffer)
                        file_hash = md5.hexdigest()
                        if file_hash == line_hash:
                            print('{}: {} and {} match'.format(fn, file_hash, line_hash))
                        else:
                            print('Hash does not match')
