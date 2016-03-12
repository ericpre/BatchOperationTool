# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 20:39:16 2015

@author: eric
"""
import os
import nose
from batch_operation_tool.delete.delete import delete_files_list_function

def test_delete_files_list_function():
    files_list_before = os.listdir('.')
    # create files
    files_list = ['file1.txt', 'file2.txt']
    for filename in files_list:
        with open(filename, 'w') as f:
            f.write("test")
    delete_files_list_function(files_list)
    files_list_after = os.listdir('.')        
    assert files_list_before == files_list_after 

if __name__ == '__main__':
    nose.run(argv=[sys.argv[0], sys.modules[__name__].__file__, '-v'])