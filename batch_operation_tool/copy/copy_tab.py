# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 16:59:12 2015

@author: eric
"""
from batch_operation_tool.base_tab.base_tab import BaseTab
from batch_operation_tool.copy.operation_widget import CopyWidget


class CopyTab(BaseTab):

    def __init__(self, fill_tables, parent=None, name="Copy files"):
        """ Need to pass the fill_tables method from parent class"""
        BaseTab.__init__(self, fill_tables=fill_tables, parent=parent)
        self.name = name

    def _initUI(self):
        self._init_baseUI()
        self.copy_widget = CopyWidget(get_files_list=self.get_files_lists,
                                      parent=self)

        self.vbox.addWidget(self.copy_widget)
        self.setLayout(self.vbox)

        self._connect_ui()
        self._connect_open_folder()

    def _connect_open_folder(self):
        self.SelectFolderButton.clicked.connect(self._set_dest_dit)

    def _set_dest_dit(self):
        self.copy_widget.set_parameters(dest_dir=self.filter_widget.dname)

    def _connect_ui(self):
        super()._connect_ui()
        self.OperationApplyButton.clicked.connect(self._copy_files)

    def _copy_files(self):
        self.copy_widget._setup_conversion()
        files_list = self.get_files_lists()[0]
        function = self.copy_widget.copy_file
        self.run_threaded_process(files_list, function)
