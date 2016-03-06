# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 12:02:32 2015

@author: eric
"""
import os
import os.path as p

from batch_operation_tool.file_filter import FileFilter
from batch_operation_tool.tests.utils_tests import remove_files, get_dirname_file, \
        create_files, substract_lists, get_all_files_including_subdirectory, listdir_absolute_path

from batch_operation_tool.tests.utils_tests import convert_file_list_absolute_path

class test_Filter():
    def setUp(self):
        parameters = {'string_list':[''],
                      'extension_list':['ext', 'ext2', 'abc'],
                      'ignore_string_bool':False,
                      'ignore_string_list':[''],
                      'ignore_string_path_bool':False,
                      'ignore_string_path_list':[''],
                      'ignore_filename_extension_bool':False,
                      'ignore_filename_extension_list':['']}
        self.tests_dir = get_dirname_file()
        self.ff = FileFilter(dname=self.tests_dir, subdirectory_bool=False, **parameters)
        fl = ['fname0.ext', 'fname1.ext', 'fname2.ext2', 'fname3.abc']
        self.fl = self._convert_file_list(sorted(fl))

    def _convert_file_list(self, file_list):
        return convert_file_list_absolute_path(file_list, self.tests_dir)

    def test_get_conditional_files_list_extension0(self):
        self.ff.extension_list = self.ff._set_extension_list('.ext')
        self.ff._get_conditional_files_list(self.fl, '')
        assert self.ff.files_to_use_list == self._convert_file_list(['fname0.ext', 'fname1.ext'])
        assert self.ff.files_to_ignore_list == self._convert_file_list(['fname2.ext2', 'fname3.abc'])

    def test_get_conditional_files_list_extension1(self):
        self.ff.extension_list = self.ff._set_extension_list('ext')
        self.ff._get_conditional_files_list(self.fl, '')
        assert self.ff.files_to_use_list == self._convert_file_list(['fname0.ext', 'fname1.ext'])
        assert self.ff.files_to_ignore_list == self._convert_file_list(['fname2.ext2', 'fname3.abc'])
    
    def test_get_conditional_files_list_extension2(self):
        self.ff.extension_list = self.ff._set_extension_list(['abc', '.ext2'])
        self.ff._get_conditional_files_list(self.fl, '')
        assert self.ff.files_to_use_list == self._convert_file_list(['fname2.ext2', 'fname3.abc'])
        assert self.ff.files_to_ignore_list == self._convert_file_list(['fname0.ext', 'fname1.ext'])

    def test_get_conditional_files_list_path0(self):
        self.ff.ignore_string_path_bool = False
        self.ff.ignore_string_path_list = self.ff._set_list(['fname'])
        self.ff._get_conditional_files_list(self.fl, '')
        assert self.ff.files_to_use_list == self.fl
        assert self.ff.files_to_ignore_list == []
      
    def test_get_conditional_files_list_path1(self):
        self.ff.ignore_string_path_bool = True
        self.ff.ignore_string_path_list = self.ff._set_list(['to_ignore'])
        self.ff._get_conditional_files_list(self.fl, 'path')
        assert self.ff.files_to_use_list == [p.join('path', l) for l in self.fl]
        assert self.ff.files_to_ignore_list == []

    def test_get_conditional_files_list_path2(self):
        self.ff.ignore_string_path_bool = True
        self.ff.ignore_string_path_list = self.ff._set_list(['to_ignore'])
        self.ff._get_conditional_files_list(self.fl, 'path_to_ignore')
        assert self.ff.files_to_use_list == []
        assert self.ff.files_to_ignore_list == [p.join('path_to_ignore', l) for l in self.fl]
      
    def test_get_conditional_files_list_path3(self):
        self.ff.ignore_string_path_bool = True
        self.ff.ignore_string_path_list = self.ff._set_list([''])
        self.ff._get_conditional_files_list(self.fl, 'path')
        assert self.ff.files_to_use_list == []
        assert self.ff.files_to_ignore_list == [p.join('path', l) for l in self.fl]

    def test_get_conditional_files_list_path4(self):
        self.ff.ignore_string_path_bool = True
        self.ff.ignore_string_path_list = self.ff._set_list(['to_ignore', 'abc'])
        self.ff._get_conditional_files_list(self.fl, 'abc')
        assert self.ff.files_to_use_list == []
        assert self.ff.files_to_ignore_list == [p.join('path', l) for l in self.fl]

    def test_get_conditional_files_list_string0(self):
        self.ff.string_list = self.ff._set_list(['fname'])
        self.ff._get_conditional_files_list(self.fl, '')
        assert self.ff.files_to_use_list == self._convert_file_list(['fname0.ext', 'fname1.ext', 'fname2.ext2', 'fname3.abc'])
        assert self.ff.files_to_ignore_list == self._convert_file_list([])

    def test_get_conditional_files_list_string1(self):
        self.ff.string_list = self.ff._set_list(['fname0', 'fname1'])
        self.ff._get_conditional_files_list(self.fl, '')
        assert self.ff.files_to_use_list == self._convert_file_list(['fname0.ext', 'fname1.ext'])
        assert self.ff.files_to_ignore_list == self._convert_file_list(['fname2.ext2', 'fname3.abc'])

    def test_get_conditional_files_list_string2(self):
        self.ff.string_list = self.ff._set_list(['file'])
        self.ff._get_conditional_files_list(self.fl, '')
        assert self.ff.files_to_use_list == self._convert_file_list([])
        assert self.ff.files_to_ignore_list == self._convert_file_list(['fname0.ext', 'fname1.ext', 'fname2.ext2', 'fname3.abc'])
    
    def test_get_files_lists(self):
        # Create files
        create_files(self.fl)
        # Expected results
        files_to_use_list = [p.join(self.tests_dir, fname) for fname in self.fl]
        list_temp = listdir_absolute_path(self.tests_dir)
        files_to_ignore_list = sorted(substract_lists(list_temp, self.fl))
        # Test
        self.ff.subdirectory_bool = False
        assert self.ff.get_files_lists()[0] == files_to_use_list
        assert self.ff.get_files_lists() == (files_to_use_list, files_to_ignore_list)
        # Remove files
        remove_files(self.fl)

    def test_get_files_lists_with_subdirectory(self):        
        # Create files
        subdirectory_name = p.join(self.tests_dir, 'tests_run')
        create_files(self.fl, subdirectory=subdirectory_name)
        # Expected results
        all_files_list = get_all_files_including_subdirectory(self.tests_dir)
        subdir = [p.join(self.tests_dir, 'tests_run', p.basename(fname)) for fname in self.fl]
        self.fl.extend(subdir)
        files_to_use_list = self.fl  
        files_to_ignore_list = substract_lists(all_files_list, files_to_use_list)
        # Test
        self.ff.subdirectory_bool = True
        assert self.ff.get_files_lists() == (files_to_use_list, files_to_ignore_list)
        remove_files(self.fl, subdirectory=subdirectory_name)    

    def test_set_extension_list(self):
        self.ff.extension_list = self.ff._set_extension_list(['ext0', '.ext1'])
        assert self.ff.extension_list == ['.ext0', '.ext1']        
        
    def test_set_list0(self):
        string = 'string'
        assert self.ff._set_list(string) == [string]

    def test_set_list1(self):
        string = ['string']
        assert self.ff._set_list(string) == string

    def test_set_list2(self):
        string = ['string0', 'string1']
        assert self.ff._set_list(string) == string

    def test_pass_string_in_fname_condition(self):
        self.ff.string_list = self.ff._set_list(['file'])
        assert self.ff._pass_string_in_fname_condition('filename') == True
        assert self.ff._pass_string_in_fname_condition('0.0.0 file name') == True
        assert self.ff._pass_string_in_fname_condition('0.0.0 file name.emi') == True
        assert self.ff._pass_string_in_fname_condition('abc') == False
        assert self.ff._pass_string_in_fname_condition('abc.emi') == False

    def test_pass_ignore_string_in_fname_condition(self):
        self.ff.ignore_string_bool = True
        self.ff.ignore_string_list = self.ff._set_list(['to_ignore'])
        assert self.ff._pass_ignore_string_in_fname_condition('filename_to_ignore') == False

        self.ff.ignore_string_bool = True
        self.ff.ignore_string_list = self.ff._set_list(['to_ignore'])
        assert self.ff._pass_ignore_string_in_fname_condition('filename') == True
    
        self.ff.ignore_string_bool = False
        self.ff.ignore_string_list = self.ff._set_list(['to_ignore'])
        assert self.ff._pass_ignore_string_in_fname_condition('filename_to_ignore') == True

        self.ff.ignore_string_bool = False
        self.ff.ignore_string_list = self.ff._set_list(['to_ignore'])
        assert self.ff._pass_ignore_string_in_fname_condition('filename') == True

    def test_pass_string_in_path_condition(self):
        self.ff.ignore_string_path_bool = True
        self.ff.ignore_string_path_list = self.ff._set_list(['to_ignore'])
        assert self.ff._pass_string_in_path_condition('path_to_ignore') == False

        self.ff.ignore_string_path_bool = True
        self.ff.ignore_string_path_list = self.ff._set_list(['to_ignore'])
        assert self.ff._pass_string_in_path_condition('path') == True

        self.ff.ignore_string_path_bool = False
        self.ff.ignore_string_path_list = self.ff._set_list(['to_ignore'])
        assert self.ff._pass_string_in_path_condition('path_to_ignore') == True          

        self.ff.ignore_string_path_bool = False
        self.ff.ignore_string_path_list = self.ff._set_list(['to_ignore'])
        assert self.ff._pass_string_in_path_condition('path') == True

        self.ff.ignore_string_path_bool = True
        self.ff.ignore_string_path_list = self.ff._set_list(['to_ignore', 'abc'])
        assert self.ff._pass_string_in_path_condition('path') == True
 
        self.ff.ignore_string_path_bool = True
        self.ff.ignore_string_path_list = self.ff._set_list(['to_ignore', 'abc'])
        assert self.ff._pass_string_in_path_condition('path_to_ignore') == False

    def test_pass_ignore_if_same_file_with_extension_condition(self):
        self.ff.ignore_filename_extension_bool = True
        self.ff.ignore_filename_extension_list = self.ff._set_list(['ext_to_ignore'])
        path = os.getcwd()
        path = self.tests_dir
        fl = self._convert_file_list(['fname.ext', 'fname.ext_to_ignore'])
        create_files(fl)
        assert self.ff._pass_ignore_if_same_file_with_extension_condition(path, p.join(path, 'fname')) == True
        remove_files(fl)

        self.ff.ignore_filename_extension_bool = True
        self.ff.ignore_filename_extension_list = self.ff._set_list(['ext_to_ignore'])
        fl = self._convert_file_list(['fname.ext', 'fname.ext2'])
        create_files(fl)
        assert self.ff._pass_ignore_if_same_file_with_extension_condition(path, p.join(path, 'fname')) == False
        remove_files(fl)

        self.ff.ignore_filename_extension_bool = False
        self.ff.ignore_filename_extension_list = self.ff._set_list(['ext_to_ignore'])
        fl = self._convert_file_list(['fname.ext', 'fname.ext_to_ignore'])
        create_files(fl)
        assert self.ff._pass_ignore_if_same_file_with_extension_condition(path, p.join(path, 'fname')) == True
        remove_files(fl)

        self.ff.ignore_filename_extension_bool = False
        self.ff.ignore_filename_extension_list = self.ff._set_list(['ext_to_ignore'])
        fl = self._convert_file_list(['fname.ext', 'fname.ext2'])
        create_files(fl)
        assert self.ff._pass_ignore_if_same_file_with_extension_condition(path, p.join(path, 'fname')) == True
        remove_files(fl)  

        self.ff.ignore_filename_extension_bool = True
        self.ff.ignore_filename_extension_list = self.ff._set_list(['ext_to_ignore1', 'ext_to_ignore2'])
        fl = self._convert_file_list(['fname.ext', 'fname.ext2'])
        create_files(fl)
        assert self.ff._pass_ignore_if_same_file_with_extension_condition(path, p.join(path, 'fname')) == False
        remove_files(fl)   

        self.ff.ignore_filename_extension_bool = True
        self.ff.ignore_filename_extension_list = self.ff._set_list(['ext_to_ignore1', 'ext_to_ignore2'])
        fl = self._convert_file_list(['fname.ext', 'fname.ext_to_ignore1'])
        create_files(fl)
        assert self.ff._pass_ignore_if_same_file_with_extension_condition(path, p.join(path, 'fname')) == True
        remove_files(fl)
        
        self.ff.ignore_filename_extension_bool = True
        self.ff.ignore_filename_extension_list = self.ff._set_list(['ext_to_ignore1', 'ext_to_ignore2'])
        fl = self._convert_file_list(['fname.ext', 'fname.ext_to_ignore2'])
        create_files(fl)
        assert self.ff._pass_ignore_if_same_file_with_extension_condition(path, p.join(path, 'fname')) == True
        remove_files(fl)

        self.ff.ignore_filename_extension_bool = True
        self.ff.ignore_filename_extension_list = self.ff._set_list(['ext_to_ignore1', 'ext_to_ignore2'])
        fl = self._convert_file_list(['fname.ext', 'fname.ext_to_ignore1', 'fname.ext_to_ignore2'])
        create_files(fl)
        assert self.ff._pass_ignore_if_same_file_with_extension_condition(path, p.join(path, 'fname')) == True
        remove_files(fl)
       
    def test_pass_extension_condition(self):
        self.ff.extension_list = self.ff._set_extension_list(['ext', '.ext'])
        assert self.ff._pass_extension_condition('.ext') == True
        assert self.ff._pass_extension_condition('.exta') == False

        self.ff.extension_list = self.ff._set_extension_list(['ext'])
        assert self.ff._pass_extension_condition('.ext') == True
        assert self.ff._pass_extension_condition('.exta') == False