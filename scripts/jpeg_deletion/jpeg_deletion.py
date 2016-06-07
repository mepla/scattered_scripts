__author__ = 'mepla'
import os
import sys

jpeg_exts = ['jpg', 'JPG', 'jpeg', 'JPEG']


def delete_jpeg_with_now_raw(path):
    to_be_deleted = []
    for file in os.listdir(path):
        try:
            name, ext = file.split('.')
        except:
            name = file
            ext = ''

        if ext in jpeg_exts:
            raf_file = name + '.RAF'
            if os.path.exists(os.path.join(path, raf_file)):
                os.remove(os.path.join(path, file))
                to_be_deleted.append(file)

    print('Deleted {} jpegs: \n'.format(len(to_be_deleted)))
    for x in to_be_deleted:
        print(x)


def print_help():
    print '[ERROR] Wrong use, use it like this: \npython jpeg_deletion.py [path_to_image_dir]'

if __name__ == '__main__':
    try:
        path = sys.argv[1]
        delete_jpeg_with_now_raw(path)
    except:
        print_help()
