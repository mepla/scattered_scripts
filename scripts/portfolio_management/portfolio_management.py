import argparse
from collections import OrderedDict

__author__ = 'mepla'
import os
import sys

jpeg_exts = ['jpg', 'JPG', 'jpeg', 'JPEG']
all_dir_name = 'All'


def jpeg_tree(path):
    all_files_categorized = {}
    all_files = os.listdir(path)
    for file_or_dir in all_files:
        sub_dir = os.path.join(path, file_or_dir)
        if not os.path.isdir(sub_dir):
            continue

        all_sub_dir_files_or_dirs = os.listdir(sub_dir)
        all_sub_dir_files = set()
        for sub_dir_file_or_dir in all_sub_dir_files_or_dirs:
            sub_dir_file_or_dir_path = os.path.join(path, file_or_dir, sub_dir_file_or_dir)
            try:
                extension = sub_dir_file_or_dir.split('.')[-1]
            except:
                extension = None

            if os.path.isfile(sub_dir_file_or_dir_path) and extension in jpeg_exts:
                all_sub_dir_files.add(sub_dir_file_or_dir)

        all_files_categorized[file_or_dir] = all_sub_dir_files

    return all_files_categorized


def analyze_jpeg_tree(tree_doc):
    all_dir_files = tree_doc.get(all_dir_name)
    all_other_dirs_files = set()
    for dir_name, files_list in tree_doc.items():
        if dir_name == all_dir_name:
            continue

        in_dir_not_in_all = sorted(files_list - all_dir_files)

        if len(in_dir_not_in_all) == 0:
            in_dir_not_in_all = ""

        print '\nFiles in {} but not in All: {}'.format(dir_name, in_dir_not_in_all)

        all_other_dirs_files = all_other_dirs_files.union(files_list)

    in_all_not_in_others = sorted(list(all_dir_files - all_other_dirs_files))
    print '\nFiles in All but not in sub directories: {}\n'.format(in_all_not_in_others)
    print '#' * 50

    tree_doc['{}-Not'.format(all_dir_name)] = all_other_dirs_files
    tree_doc = OrderedDict(sorted(tree_doc.items()))

    max_lenght_name = max(len(x) for x in tree_doc.keys())
    for dir_name, files_list in tree_doc.items():
        middle_string = ': '
        needed_spaces = max_lenght_name - len(dir_name) + 2
        print '{}{}{}{}'.format(dir_name, middle_string, ' ' * needed_spaces, len(files_list))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', action="store", dest="path", default=None,
                        help="Path to portfolio directory")

    args = parser.parse_args()

    print args.path
    if args.path:
        tree_result = jpeg_tree(args.path)
        analyze_jpeg_tree(tree_result)
    else:
        parser.print_help()

