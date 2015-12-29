# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 14:32:20 2015

@author: eric
"""

import os
from python_qt_binding import QtGui
import json

import batch_operation_tool
from batch_operation_tool.base_tab.filter_widget_base import FilterWidgetBase

class BaseTab(QtGui.QWidget):    
    def __init__(self, fill_tables, parent=None):
        """ Need to pass the fill_tables method from parent class"""
        super(BaseTab, self).__init__(parent=parent)
        self._initUI()
        self._init_main_parameters()
        self.fill_tables = fill_tables
        
    def _initUI(self):
        self.filter_widget = FilterWidgetBase(parent=self)
        
        self.SelectFolderButton = QtGui.QPushButton('Select folder', self)
        self.SubdirectoryCheckBox = QtGui.QCheckBox('Subdirectory:', self)
        self.OperationApplyButton = QtGui.QPushButton('Delete files', self)    
        self.LoadConfigButton = QtGui.QPushButton('Load config', self)  
        self.SaveConfigButton = QtGui.QPushButton('Save config', self)  

        # layout
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.SelectFolderButton)
        hbox1.addWidget(self.SubdirectoryCheckBox)
        hbox1.addWidget(self.OperationApplyButton)
        hbox1.addWidget(self.LoadConfigButton)
        hbox1.addWidget(self.SaveConfigButton)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addWidget(self.filter_widget)
        self.setLayout(vbox)
        
    def _connect_ui(self):
        pass

    def _init_main_parameters(self, subdirectory=False):
        self.main_parameters = {'directory':self.get_dname(),
                                'subdirectory':subdirectory}        

    def load_config(self, fname=None):
        if fname is None:
            fname = os.path.join(self._get_library_path(), 'delete',
                                 'default_settings.json')
        with open(fname, "r") as data_file:
            config = json.load(data_file)
        main_parameters = config['Main']
        filter_parameters = config['Filter']
        self._set_main_parameters(**main_parameters)
        self.set_filter_parameters(**filter_parameters)
    
    def _get_library_path(self):
        return os.path.dirname(batch_operation_tool.__file__)

    def _save_config(self, fname=None):
        if fname is None:
            fname = os.path.join(self._get_library_path(), 'EMS_file_conversion',
                                 'default_setting.json')
        config = {'Main':self._get_main_parameters(),
                  'Filter':self.filter_widget.get_parameters()}
        with open(fname, 'w') as outfile:
            json.dump(config, outfile)
            
    def _set_main_parameters(self, **params):
        if params['directory'] is None:
            params['directory'] = os.getcwd()
        self.set_dname(params['directory'])
        self.set_subdirectory(params['subdirectory'])

    def _get_main_parameters(self):
        self.main_parameters = {'directory':self.get_dname(),
                                'subdirectory':self.get_subdirectory()}
        return self.main_parameters

    def _update_subdirectory(self):
        self.set_subdirectory(self.SubdirectoryCheckBox.isChecked())
        self.get_files_lists()
        self.fill_tables()
        
    def get_files_lists(self):
        self.filter_widget.update_files_lists()
        self.files_to_use_list, self.files_to_ignore_list = self.filter_widget.get_files_lists()
        return self.files_to_use_list, self.files_to_ignore_list
        
    def set_subdirectory(self, value):
        self.main_parameters['subdirectory'] = value
        self.SubdirectoryCheckBox.setChecked(value)

    def get_subdirectory(self):
        return self.main_parameters['subdirectory']

    def set_filter_parameters(self, **params):
        self.filter_widget.set_parameters(**params)
        
    def set_dname(self, dname):
        self.main_parameters['directory'] = os.path.expanduser(dname)
        self.filter_widget.set_dname(dname)

    def get_dname(self):
        return self.filter_widget.dname

    def _load_config_dialog(self):
        dname0 = self.get_dname()
        fname = str(QtGui.QFileDialog.getOpenFileName(self, directory=dname0,
                                                      filter='*.json')[0])
        if fname is '':
            return
        else:
            self.load_config(fname=fname)

    def _save_config_dialog(self):
        dname0 = self.get_dname()
        fname = str(QtGui.QFileDialog.getSaveFileName(self, directory=dname0,
                                                      filter='*.json')[0])
        if fname is '':
            return
        else:
            self._save_config(fname=fname)

    def _open_directory_dialog(self):
        dname0 = self.get_dname()
        dname = str(QtGui.QFileDialog.getExistingDirectory(self, directory=dname0))
        if dname is '':
            dname = dname0
        self.set_dname(dname)
        self.get_files_lists()
        self.fill_tables()