# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 15:02:36 2015

@author: eric
"""

import os
from qtpy import QtWidgets
import json

from batch_operation_tool.base_tab.base_tab import BaseTab
from batch_operation_tool.TIA_file_conversion.filter_widget import FilterWidget
from batch_operation_tool.TIA_file_conversion.operation_widget import TIAConversionWidget


class TIAConversionTab(BaseTab):

    def __init__(self, fill_tables, name="TIA/Velox conversion", parent=None):
        """ Need to pass the fill_tables method from parent class"""
        super(TIAConversionTab, self).__init__(
            fill_tables=fill_tables, parent=parent)
        self.name = name

    def _initUI(self):
        self.filter_widget = FilterWidget(parent=self)
        self.tia_conversion_widget = TIAConversionWidget(get_files_list=self.get_files_lists,
                                                         parent=self)

        self.SelectFolderButton = QtWidgets.QPushButton('Select folder', self)
        self.SubdirectoryCheckBox = QtWidgets.QCheckBox('Subdirectory:', self)
        self.OperationApplyButton = QtWidgets.QPushButton('Convert', self)
        self.LoadConfigButton = QtWidgets.QPushButton('Load config', self)
        self.SaveConfigButton = QtWidgets.QPushButton('Save config', self)

        # layout
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self.SelectFolderButton)
        hbox1.addWidget(self.SubdirectoryCheckBox)
        hbox1.addWidget(self.OperationApplyButton)
        hbox1.addWidget(self.LoadConfigButton)
        hbox1.addWidget(self.SaveConfigButton)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addWidget(self.filter_widget)
        vbox.addWidget(self.tia_conversion_widget)
        self.setLayout(vbox)

        self._connect_ui()

    def _connect_ui(self):
        self.SelectFolderButton.clicked.connect(self._open_directory_dialog)
        self.SubdirectoryCheckBox.clicked.connect(self._update_subdirectory)
        self.OperationApplyButton.clicked.connect(self._convert_files)
        self.LoadConfigButton.clicked.connect(self._load_config_dialog)
        self.SaveConfigButton.clicked.connect(self._save_config_dialog)

    def load_config(self, fname=None):
        if fname is None:
            fname = os.path.join(self._get_library_path(), 'TIA_file_conversion',
                                 'default_settings.json')
        with open(fname, "r") as data_file:
            config = json.load(data_file)
        main_parameters = config['Main']
        filter_parameters = config['Filter']
        operation_parameters = config['Operation']
        self._set_main_parameters(**main_parameters)
        self.set_filter_parameters(**filter_parameters)
        self.set_operation_parameters(**operation_parameters)

    def _save_config(self, fname=None):
        if fname is None:
            fname = os.path.join(self._get_library_path(), 'TIA_file_conversion',
                                 'default_setting.json')
        config = {'Main': self._get_main_parameters(),
                  'Filter': self.filter_widget.get_parameters(),
                  'Operation': self.tia_conversion_widget.get_parameters()}
        with open(fname, 'w') as outfile:
            json.dump(config, outfile)

    def set_operation_parameters(self, **params):
        self.tia_conversion_widget.set_parameters(**params)

    def _convert_files(self):
        # Add dialog box to confirm?
        #        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        #        buttonBox.show()
        self.tia_conversion_widget._setup_conversion()
        files_list = self.get_files_lists()[0]
        function = self.tia_conversion_widget.convert_file
        self.run_threaded_process(files_list, function)