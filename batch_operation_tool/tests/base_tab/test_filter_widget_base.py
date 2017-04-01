# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 12:43:18 2015

@author: eric
"""
import sys
from qtpy import QtWidgets

from batch_operation_tool.base_tab.base_tab import BaseTab
from batch_operation_tool.delete.delete_tab import DeleteTab
from batch_operation_tool.base_tab.filter_widget_base import FilterWidgetBase
from batch_operation_tool.batch_operation_tool_ui import BatchOperationToolUI

from batch_operation_tool.tests.utils_tests import get_dirname_file
from batch_operation_tool.tests.utils_tests import convert_file_list_absolute_path

class Test_FilterWidgetBase:
    @classmethod
    def setup_class(self):
        self.app = QtWidgets.QApplication(sys.argv)

    @classmethod
    def teardown_class(self):
        self.app.quit()
    
    def setup_method(self):
        self.parameters = {'string_list':[''],
                           'extension_list':['ext', 'ext2', 'abc'],
                           'ignore_string_bool':False,
                           'ignore_string_list':[''],
                           'ignore_string_path_bool':False,
                           'ignore_string_path_list':[''],
                           'ignore_filename_extension_bool':False,
                           'ignore_filename_extension_list':['']}
        self.tests_dir = get_dirname_file()
        self.botui = BatchOperationToolUI(load_settings=None)
        self.botui.add_tab(DeleteTab)
        self.bt = BaseTab(self.botui.fill_tables, parent=self.botui)
        self.fw = FilterWidgetBase(parent=self.bt)
        self.fw.dname = self.tests_dir
        self.fl_short = ['fname0.ext', 'fname1.ext', 'fname2.ext2', 'fname3.abc']
        self.fl = self._convert_file_list(sorted(self.fl_short))

    def _convert_file_list(self, file_list):
        return convert_file_list_absolute_path(file_list, self.tests_dir)
    
    def test_set_parameter(self):
        self.fw.set_parameters(**self.parameters)
        assert self.fw.parameters['string_list'] == self.fw.stringLineEdit.text().split(', ')
        assert self.fw.parameters['extension_list'] == self.fw.extentionLineEdit.text().split(', ')
        assert self.fw.parameters['ignore_string_bool'] == self.fw.ignoreStringCheckBox.isChecked()
        assert self.fw.parameters['ignore_string_list'] == self.fw.ignoreStringLineEdit.text().split(', ')
        assert self.fw.parameters['ignore_string_path_bool'] == self.fw.ignoreStringPathCheckBox.isChecked()
        assert self.fw.parameters['ignore_string_path_list'] == self.fw.ignoreStringPathLineEdit.text().split(', ')
        assert self.fw.parameters['ignore_filename_extension_bool'] == self.fw.ignorefilenameextensionCheckBox.isChecked()
        assert self.fw.parameters['ignore_filename_extension_list'] == self.fw.ignorefilenameextensionLineEdit.text().split(', ')

    def test_get_parameter(self):
        self.fw.set_parameters(**self.parameters)
        assert self.parameters == self.fw.get_parameters()   
    
#    def test_update_files_lists(self):
#        # Create files
#        create_files(self.fl)
#        self.fw.set_parameters(**self.parameters)
#        self.fw.set_parameters(string_list=self.fl_short)
#        print self.fw.dname, self.fw.parameters['string_list']
#        self.fw.update_files_lists()
#        # Expected results
#        files_to_use_list = [os.path.join(self.tests_dir, fname) for fname in self.fl]
#        files_to_ignore_list = substract_lists(os.listdir('.'), self.fl)
#
#        list_temp = listdir_absolute_path(self.tests_dir)
#        files_to_ignore_list = sorted(substract_lists(list_temp, self.fl))
#
#        print '1:', len(files_to_use_list), files_to_use_list
#        print '12:', len(self.fw.files_to_use_list), self.fw.files_to_use_list
##        print '2:', len(files_to_ignore_list), files_to_ignore_list
##        print '22:', len(self.fw.get_files_lists()[1]), self.fw.get_files_lists()[1]     
#        
#        assert self.fw.get_files_lists() == (files_to_use_list, files_to_ignore_list)
#        # Remove files
#        remove_files(self.fl)    
       
    def test_get_subdirectory(self):
        subdirectory = self.bt.get_subdirectory()
        assert subdirectory == self.fw._get_subdirectory()
        
    def test_dname(self):
        dname = 'dummy_dname'
        self.fw.dname = dname
        assert self.fw.dname == dname

if __name__ == '__main__':
    import pytest
    pytest.main()