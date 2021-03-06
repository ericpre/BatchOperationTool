# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 16:59:12 2015

@author: eric
"""
import os
import json

from batch_operation_tool.base_tab.base_tab import BaseTab
from batch_operation_tool.EMS_conversion.operation_widget import EMSConversionWidget


class EMSConversionTab(BaseTab):

    def __init__(self, fill_tables, name="EMS conversion", parent=None):
        """ Need to pass the fill_tables method from parent class"""
        super(EMSConversionTab, self).__init__(
            fill_tables=fill_tables, parent=parent)
        self.name = name

    def _initUI(self):
        self._init_baseUI()
        self.OperationApplyButton.setText('Convert')
        self.ems_conversion_widget = EMSConversionWidget(get_files_list=self.get_files_lists,
                                                         parent=self)
        self.vbox.addWidget(self.ems_conversion_widget)
        self.setLayout(self.vbox)

        self._connect_ui()

    def _connect_ui(self):
        super()._connect_ui()
        self.OperationApplyButton.clicked.connect(self._convert_files)

    def load_config(self, fname=None):
        if fname is None:
            fname = os.path.join(self._get_library_path(), 'EMS_conversion',
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
            fname = os.path.join(self._get_library_path(), 'EMS_conversion',
                                 'default_setting.json')
        config = {'Main': self._get_main_parameters(),
                  'Filter': self.filter_widget.get_parameters(),
                  'Operation': self.ems_conversion_widget.get_parameters()}
        with open(fname, 'w') as outfile:
            json.dump(config, outfile)

    def set_operation_parameters(self, **params):
        self.ems_conversion_widget.set_parameters(**params)

    def _convert_files(self):
        self.ems_conversion_widget._setup_conversion()
        files_list = self.get_files_lists()[0]
        function = self.ems_conversion_widget.convert_file
        self.run_threaded_process(files_list, function)
