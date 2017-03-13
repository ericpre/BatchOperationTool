# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 15:24:46 2015

@author: eric
"""
import os
import shutil


def copy_files(files_list, dest_dir, keep_original=True):
    makedir(dest_dir)
    # remove filename in dest_dir from files_list
    files_list = [fname for fname in files_list if dest_dir not in fname]
    string = 'Moving'
    if keep_original:
        string = 'Copying'
    for i, filename in enumerate(files_list):
        print('%s file #%i: %s' % (string, i, filename))
        common_path = os.path.commonpath([filename, dest_dir])
        dest_subdir = filename.split(common_path)[1][1:]
        kwargs = {'src': filename,
                  'dst': os.path.join(dest_dir, dest_subdir)}
        path_split = os.path.split(dest_subdir)[0]
        if len(path_split) > 0:
            makedir(os.path.join(dest_dir, path_split))
        if keep_original:
            shutil.copy(**kwargs)
        else:
            shutil.move(**kwargs)


def makedir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
