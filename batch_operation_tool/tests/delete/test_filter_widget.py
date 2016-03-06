# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 11:22:46 2015

@author: eric
"""
import sys, os
from python_qt_binding import QtGui

from batch_operation_tool.delete.filter_widget import FilterWidget
from batch_operation_tool.delete.delete_tab import DeleteTab
from batch_operation_tool.batch_operation_tool_ui import BatchOperationToolUI

class test_FilterWidget:
    @classmethod
    def setup_class(self):
        self.app = QtGui.QApplication(sys.argv)

    @classmethod
    def teardown_class(self):
        self.app.quit()
    
    def setUp(self):
        self.parameters = {'string_list':[''],
                           'extension_list':['ext', 'ext2', 'abc'],
                          'ignore_string_bool':False,
                          'ignore_string_list':[''],
                          'ignore_string_path_bool':False,
                          'ignore_string_path_list':[''],
                          'ignore_filename_extension_bool':False,
                          'ignore_filename_extension_list':['']}
        self.botui = BatchOperationToolUI(load_settings=None)
        name ='Delete files'
        self.botui.add_tab(DeleteTab, name=name)
        self.fw = FilterWidget(parent=self.botui.tab[name])
        self.fl = ['fname0.ext', 'fname1.ext', 'fname2.ext2', 'fname3.abc']
    
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