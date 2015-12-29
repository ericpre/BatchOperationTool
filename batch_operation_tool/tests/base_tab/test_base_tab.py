# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 12:28:39 2015

@author: eric
"""
import sys, os, json
from python_qt_binding import QtGui

from batch_operation_tool.base_tab.base_tab import BaseTab
from batch_operation_tool.batch_operation_tool_ui import BatchOperationToolUI
from batch_operation_tool.tests.utils_tests import merge_two_dicts

class test_BaseTab:
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
        self.bt = BaseTab(self.botui.fill_tables, parent=self.botui)

    def test_init_main_parameters(self):
        self.bt._init_main_parameters(False)
        assert self.bt.main_parameters['directory'] == os.getcwd()
        assert self.bt.main_parameters['subdirectory'] == False

        self.bt._init_main_parameters(True)
        assert self.bt.main_parameters['directory'] == os.getcwd()
        assert self.bt.main_parameters['subdirectory'] == True
        
    def test_load_config(self):       
        config_fname = 'default_settings.json'
        path = os.path.join(os.path.dirname(__file__))
        self.bt.load_config(os.path.join(path, config_fname))
        assert self.bt.main_parameters['directory'] == os.path.expanduser("~")
        assert self.bt.main_parameters['subdirectory'] == True

        assert self.bt.filter_widget.parameters['string_list'] == [""]
        assert self.bt.filter_widget.parameters['extension_list'] == [""]
        assert self.bt.filter_widget.parameters['ignore_string_bool'] == False
        assert self.bt.filter_widget.parameters['ignore_string_list'] == [""]
        assert self.bt.filter_widget.parameters['ignore_string_path_bool'] == False
        assert self.bt.filter_widget.parameters['ignore_string_path_list'] == [""]
        assert self.bt.filter_widget.parameters['ignore_filename_extension_bool'] == False
        assert self.bt.filter_widget.parameters['ignore_filename_extension_list'] == [""]
        
    def test_save_config(self):
        # setting parameters
        self.bt._set_main_parameters(**self.main_parameters)
        self.bt.set_filter_parameters(**self.filter_parameters)
        parameters = merge_two_dicts(self.main_parameters, self.filter_parameters)
        # saving parameters
        fname = 'test_save_config.json'
        self.bt._save_config(fname)
        # test
        with open(fname, "r") as data_file:
            config = json.load(data_file)
        config_parameters = merge_two_dicts(config['Main'], config['Filter'])

        for key in config_parameters.keys():
            assert config_parameters[key] == parameters[key]

        os.remove(fname)

    def test_set_main_parameters(self):      
        self.bt._set_main_parameters(**self.main_parameters)
        for key in self.main_parameters.keys():
            assert self.bt.main_parameters[key] == self.main_parameters[key]
    
    def test_get_main_parameters(self):   
        self.bt._set_main_parameters(**self.main_parameters)
        assert self.main_parameters == self.bt._get_main_parameters()

    def test_update_subdirectory(self):
        pass
    
    def test_get_files_lists(self):
        pass

    def test_set_filter_parameters(self):
        self.bt.set_filter_parameters(**self.filter_parameters)
        for key in self.filter_parameters.keys():
            assert self.bt.filter_widget.parameters[key] == self.filter_parameters[key]
    
    def test_set_dname(self):
        dname = 'dummy_dname'
        self.bt.set_dname(dname)
        assert self.bt.filter_widget.dname == dname

    def test_get_dname(self):
        dname = 'dummy_dname'
        self.bt.set_dname(dname)
        assert self.bt.get_dname() == dname
        
    def test_set_subdirectory(self):
        subdirectory = True
        self.bt.set_subdirectory(subdirectory)
        assert self.bt.main_parameters['subdirectory'] == subdirectory
    
    def test_get_subdirectory(self):
        subdirectory = True
        self.bt.set_subdirectory(subdirectory)
        assert self.bt.get_subdirectory() == subdirectory
