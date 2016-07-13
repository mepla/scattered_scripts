import argparse

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', action="store", dest="path", default=None,
                        help="Path to directory to delete excessive JPG files.")

    args = parser.parse_args()

    print args.path
    if args.path:
        delete_jpeg_with_now_raw(args.path)
    else:
        parser.print_help()

