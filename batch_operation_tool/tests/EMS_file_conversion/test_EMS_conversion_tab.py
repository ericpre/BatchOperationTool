# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 14:55:06 2015

@author: eric
"""
import sys, os, json
from python_qt_binding import QtGui

from batch_operation_tool.EMS_file_conversion.EMS_conversion_tab import EMSConversionTab
from batch_operation_tool.batch_operation_tool_ui import BatchOperationToolUI

from batch_operation_tool.tests.utils_tests import get_dirname_file, merge_two_dicts

class test_EMSConversionTab:
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
                                  'ignore_string_path_list':['']}
        self.main_parameters = {'subdirectory':True,
                                'directory':os.getcwd()}  
        self.operation_parameters = {'extension_list':[],
                                     'data_type':'image',
                                     'log_to_linear_scale':True,
                                     'overwrite':False}
        
        self.botui = BatchOperationToolUI(load_settings=None)
        name ='EMS conversion'
        self.botui.add_tab(EMSConversionTab, name=name)
        self.emsct = self.botui.tab[name]

    def test_set_filter_parameters(self):
        self.emsct.set_filter_parameters(**self.filter_parameters)
        for key in self.filter_parameters.keys():
            assert self.emsct.filter_widget.parameters[key] == self.filter_parameters[key]

    def test_set_operation_parameters(self):
        self.emsct.set_operation_parameters(**self.operation_parameters)
        for key in self.operation_parameters.keys():
            assert self.emsct.ems_conversion_widget.parameters[key] == self.operation_parameters[key]

    def test_load_config(self):       
        config_fname = 'default_settings.json'
        path = get_dirname_file(__file__)
        self.emsct.load_config(os.path.join(path, config_fname))
        assert self.emsct.main_parameters['directory'] == os.path.expanduser("~")
        assert self.emsct.main_parameters['subdirectory'] == False

        assert self.emsct.filter_widget.parameters['string_list'] == [""]
        assert self.emsct.filter_widget.parameters['extension_list'] == [""]
        assert self.emsct.filter_widget.parameters['ignore_string_bool'] == False
        assert self.emsct.filter_widget.parameters['ignore_string_list'] == [""]
        assert self.emsct.filter_widget.parameters['ignore_string_path_bool'] == False
        assert self.emsct.filter_widget.parameters['ignore_string_path_list'] == [""]

        assert self.emsct.ems_conversion_widget.parameters['extension_list'] == []
        assert self.emsct.ems_conversion_widget.parameters['data_type'] == 'image'
        assert self.emsct.ems_conversion_widget.parameters['log_to_linear_scale'] == True
        assert self.emsct.ems_conversion_widget.parameters['overwrite'] == False
        
    def test_save_config(self):
        # setting parameters
        self.emsct._set_main_parameters(**self.main_parameters)
        self.emsct.set_filter_parameters(**self.filter_parameters)
        self.emsct.set_operation_parameters(**self.operation_parameters)
        parameters = merge_two_dicts(self.main_parameters, self.filter_parameters)
        # saving parameters
        fname = 'test_save_config.json'
        self.emsct._save_config(fname)
        # test
        with open(fname, "r") as data_file:
            config = json.load(data_file)
        config_parameters = merge_two_dicts(config['Main'], config['Filter'])

        for key in config_parameters.keys():
            assert config_parameters[key] == parameters[key]

        os.remove(fname)
