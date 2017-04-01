# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 15:29:20 2015

@author: eric
"""
import os

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def create_files(files_list, subdirectory=None):
    files_list = files_list[:]
    if subdirectory is not None:
        os.mkdir(subdirectory)
        files_list.extend([os.path.join(subdirectory, os.path.basename(fname)) for fname in files_list])
    for fname in files_list:
        with open(fname, 'w') as f:
            f.write('test')
            
def remove_files(files_list, subdirectory=None):
    for fname in files_list:
        os.remove(fname)
    if subdirectory is not None:
        os.rmdir(subdirectory)

def substract_lists(list1, list2):
    return [fname for fname in list1 if fname not in list2]

def get_all_files_including_subdirectory(directory):
    l = []
    for root, subFolder, files_list in os.walk(directory):
        for name in files_list:
            l.append(os.path.join(root, name))
    return sorted(l)
    
def get_dirname_file(file=None):
    if file is None:
        file = __file__
    return os.path.dirname(file)

def convert_file_list_absolute_path(file_list, root_dir=None):
    if root_dir is None:
        return [os.path.join(os.path.split(os.path.abspath(fname))[0], fname) for fname in file_list]
    else:
        return [os.path.join(root_dir, fname) for fname in file_list]
        

def listdir_absolute_path(rootdir):  
    file_list = os.listdir(rootdir)
    return [os.path.join(rootdir, fname) for fname in file_list]

def listdir_absolute_path_recursive(rootdir):  
    file_paths = []
    for folder, subs, files in os.walk(rootdir):
      for filename in files:
        file_paths.append(os.path.abspath(os.path.join(folder, filename)))
    return file_paths