# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 15:24:46 2015

@author: eric
"""
import os

def delete_files_list_function(files_list):
    for i, filename in enumerate(files_list):
        print('Delete file #%i: %s'%(i, filename))
        os.remove(filename)