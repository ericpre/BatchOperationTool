# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 15:30:41 2015

@author: eric
"""
import sys, os
from python_qt_binding import QtGui

from batch_operation_tool.delete.delete_tab import DeleteTab
from batch_operation_tool.batch_operation_tool_ui import BatchOperationToolUI

class test_DeleteTab:
    @classmethod
    def setup_class(self):
        self.app = QtGui.QApplication(sys.argv)

    @classmethod
    def teardown_class(self):
        self.app.quit()

    def setUp(self):
        self.filter_parameters = {'string_list':[''],
                                  'extension_list':['ext', 'ext2', 'abc'],
                                  'ignore_string_bool':False,
                                  'ignore_string_list':[''],
                                  'ignore_string_path_bool':False,
                                  'ignore_string_path_list':[''],
                                  'ignore_filename_extension_bool':False,
                                  'ignore_filename_extension_list':['']}
        self.main_parameters = {'subdirectory':True,
                                'directory':os.getcwd()}  

        self.botui = BatchOperationToolUI(load_settings=None)
        self.dt = DeleteTab(self.botui.fill_tables, parent=self.botui)
        self.fl = ['fname0.ext', 'fname1.ext', 'fname2.ext2', 'fname3.abc']
        
    def test_set_filter_parameters(self):
        self.dt.set_filter_parameters(**self.filter_parameters)
        for key in self.filter_parameters.keys():
            assert self.dt.filter_widget.parameters[key] == self.filter_parameters[key]