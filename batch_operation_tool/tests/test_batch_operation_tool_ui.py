# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 20:53:25 2015

@author: eric
"""
import sys, os
from nose.tools import raises
from python_qt_binding import QtGui

from batch_operation_tool.batch_operation_tool_ui import BatchOperationToolUI
from batch_operation_tool.delete.delete_tab import DeleteTab
from batch_operation_tool.EMS_file_conversion.EMS_conversion_tab import EMSConversionTab

class test_BatchOperationToolUI:
    @classmethod
    def setup_class(self):
        self.app = QtGui.QApplication(sys.argv)

    @classmethod
    def teardown_class(self):
        self.app.quit()

    def setUp(self):
        self.botui = BatchOperationToolUI()
        # match the default_settings.json files from the library
        self.dt_filter_parameters = {'string_list':[''],
                                     'extension_list':[''],
                                     'ignore_string_bool':False,
                                     'ignore_string_list':[''],
                                     'ignore_string_path_bool':False,
                                     'ignore_string_path_list':[''],
                                     'ignore_filename_extension_bool':False,
                                     'ignore_filename_extension_list':['']}
        self.dt_main_parameters = {'subdirectory':False,
                                   'directory':os.getcwd()}
        self.emst_filter_parameters = {'string_list':[''],
                                       'extension_list':[''],
                                       'ignore_string_bool':False,
                                       'ignore_string_list':[''],
                                       'ignore_string_path_bool':False,
                                       'ignore_string_path_list':[''],
                                       'ignore_filename_extension_bool':False,
                                       'ignore_filename_extension_list':['']}
        self.emst_main_parameters = {'subdirectory':False,
                                     'directory':self.botui.ems_conversion_tab.get_dname()}

    def test_create_header_tabs_loading_None(self):
        self.botui._create_header_tabs(load_settings=None)
        assert type(self.botui.ems_conversion_tab) == EMSConversionTab
        assert type(self.botui.delete_tab) == DeleteTab

    def test_create_header_tabs_loading_default(self):
        self.botui._create_header_tabs(load_settings='default')
        assert type(self.botui.ems_conversion_tab) == EMSConversionTab
        assert type(self.botui.delete_tab) == DeleteTab
#        assert self.botui.delete_tab.filter_widget.get_parameters() == self.dt_filter_parameters
#        assert self.botui.delete_tab._get_main_parameters() == self.dt_main_parameters
#        assert self.botui.ems_conversion_tab.filter_widget.get_parameters() == self.emst_filter_parameters
#        assert self.botui.ems_conversion_tab._get_main_parameters() == self.emst_main_parameters

    @raises(ValueError)
    def test_create_header_tabs_loading_exception(self):
        self.botui._create_header_tabs('')
        assert type(self.botui.ems_conversion_tab) == EMSConversionTab
        assert type(self.botui.delete_tab) == DeleteTab
        
    def test_create_tables_widget(self):
        assert type(self.botui.tables_widget) == QtGui.QTabWidget
        assert self.botui.tables_widget.widget(0) == self.botui.files_table
        assert self.botui.tables_widget.widget(1) == self.botui.ignore_table
    
    def test_setup_tables(self):
        assert type(self.botui.files_table) == QtGui.QTableWidget
        assert type(self.botui.ignore_table) == QtGui.QTableWidget

    def test_fill_table_files(self):
        self._fill_table(self.botui.files_table)
        self._fill_table(self.botui.ignore_table)

    def _fill_table(self, table):
        fl = ['fname0.ext', 'fname1.ext', 'fname2.ext2', 'fname3.abc']
        table = self.botui.files_table
        fl = [os.getcwd()+ fname for fname in fl]
        self.botui._fill_table(table, fl)
        assert table.rowCount() == len(fl)
        for i, fullfilename in enumerate(fl):
            fulldirname, filename = os.path.split(fullfilename)
            path, dirname = os.path.split(fulldirname)
            assert table.item(i, 0).text() == path
            assert table.item(i, 1).text() == dirname
            assert table.item(i, 2).text() == filename
        
    def test_get_current_tab_widget(self):
        self.botui._create_header_tabs()
        self.botui.headers_tab.setCurrentWidget(self.botui.delete_tab)
        assert self.botui._get_current_tab_widget() == self.botui.delete_tab
        self.botui.headers_tab.setCurrentWidget(self.botui.ems_conversion_tab)
        assert self.botui._get_current_tab_widget() == self.botui.ems_conversion_tab