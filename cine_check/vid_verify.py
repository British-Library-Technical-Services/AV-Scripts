import os
import glob
import hashlib


def verify(dest, file, copied_register):

    dest_loc = os.path.join(dest, file)
    verify_files = glob.glob(dest_loc + '/**/*.dpx', recursive=True)

    for ver in verify_files:
        if os.path.isdir(ver):
            continue
        else:
            if not os.path.isfile(copied_register):
                print('{} not found in register'.format(copied_register))
                break
            else:
                fn = os.path.basename(ver)
                with open(copied_register, 'r') as hash_verification:
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
                                    print('VERIFIED: {} hash {}'.format(fn, file_hash))
                                else:
                                    print('FAILED: {} hash {}'.format(fn, file_hash))
