#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 17:50:13 2017

@author: eric
"""

import os, sys
import nose
import tempfile
from batch_operation_tool.copy.copy import copy_files


class TestCopy:
    
    def test_copy_files_keep_original(self):

        with tempfile.TemporaryDirectory() as tmp:           
            files_list = ['file1.txt', 'file2.txt']            
            for i, filename in enumerate(files_list):
                files_list[i] = os.path.join(tmp, filename)
                with open(files_list[i], 'w') as f:
                    f.write("test")

            files_list_original = os.listdir(tmp)
            dest_dir = os.path.join(tmp, 'copy_there')
            os.makedirs(dest_dir)

            copy_files(files_list,
                       dest_dir=dest_dir,
                       keep_original=True)
            assert os.listdir(dest_dir) == files_list_original
            files_list_original.insert(0, 'copy_there')
            assert os.listdir(tmp) == files_list_original

    def test_copy_files(self):

        with tempfile.TemporaryDirectory() as tmp:           
            files_list = ['file1.txt', 'file2.txt']            
            for i, filename in enumerate(files_list):
                files_list[i] = os.path.join(tmp, filename)
                with open(files_list[i], 'w') as f:
                    f.write("test")

            files_list_original = os.listdir(tmp)
            dest_dir = os.path.join(tmp, 'copy_there')
            os.makedirs(dest_dir)

            copy_files(files_list,
                       dest_dir=dest_dir,
                       keep_original=False)
            assert os.listdir(dest_dir) == files_list_original
            assert os.listdir(tmp) == ['copy_there'] 

    
    def test_copy_files_keep_original_subfolder(self):

        with tempfile.TemporaryDirectory() as tmp:           
            files_list = ['file1.txt', 'file2.txt']
            subdir = 'subdir'            
            os.makedirs(os.path.join(tmp, subdir))
            for i, filename in enumerate(files_list):
                files_list[i] = os.path.join(tmp, subdir, filename)
                with open(files_list[i], 'w') as f:
                    f.write("test")

            files_list_original = os.listdir(os.path.join(tmp, subdir))
            dest_dir = os.path.join(tmp, 'copy_there')
            os.makedirs(dest_dir)

            copy_files(files_list,
                       dest_dir=dest_dir,
                       keep_original=True)
            assert os.listdir(os.path.join(dest_dir, subdir)) == files_list_original
            assert os.listdir(os.path.join(tmp, subdir)) == files_list_original

    def test_copy_files_subfolder(self):

        with tempfile.TemporaryDirectory() as tmp:           
            files_list = ['file1.txt', 'file2.txt']            
            subdir = 'subdir'            
            os.makedirs(os.path.join(tmp, subdir))
            for i, filename in enumerate(files_list):
                files_list[i] = os.path.join(tmp, subdir, filename)
                with open(files_list[i], 'w') as f:
                    f.write("test")

            files_list_original = os.listdir(os.path.join(tmp, subdir))
            dest_dir = os.path.join(tmp, 'copy_there')
            os.makedirs(dest_dir)

            copy_files(files_list,
                       dest_dir=dest_dir,
                       keep_original=False)
            assert os.listdir(os.path.join(dest_dir, subdir)) == files_list_original
            assert os.listdir(os.path.join(tmp, subdir)) == []          

if __name__ == '__main__':
    nose.run(argv=[sys.argv[0], sys.modules[__name__].__file__, '-v'])