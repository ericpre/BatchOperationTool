# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 15:24:46 2015

@author: eric
"""
import os
import shutil


class CopyFiles:

    def __init__(self, dest_dir=None, keep_original=True):
        self.dest_dir = dest_dir
        self.keep_original = keep_original
        self.fname = None

    def copy_file(self):
        if self.fname is None:
            # Filename needs to be set when calling this method
            raise ValueError("Filename error, please report the issue")
        makedir(self.dest_dir)
        common_path = os.path.commonpath([self.fname, self.dest_dir])
        dest_subdir = self.fname.split(common_path)[1][1:]
        kwargs = {'src': self.fname,
                  'dst': os.path.join(self.dest_dir, dest_subdir)}
        path_split = os.path.split(dest_subdir)[0]
        if len(path_split) > 0:
            makedir(os.path.join(self.dest_dir, path_split))
        if self.keep_original:
            shutil.copy(**kwargs)
        else:
            shutil.move(**kwargs)


def makedir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
