# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 16:59:12 2015

@author: eric
"""
import os

from qtpy import QtWidgets

from batch_operation_tool.base_tab.base_tab import BaseTab
from batch_operation_tool.delete.filter_widget import FilterWidget


class DeleteTab(BaseTab):

    def __init__(self, fill_tables, parent=None, name="Delete files"):
        """ Need to pass the fill_tables method from parent class"""
        BaseTab.__init__(self, fill_tables=fill_tables, parent=parent)
        self.name = name
#        self._initUI()
#        self._init_main_parameters()
#        self.fill_tables = fill_tables

    def _initUI(self):
        self.filter_widget = FilterWidget(parent=self)

        self.SelectFolderButton = QtWidgets.QPushButton('Select folder', self)
        self.SubdirectoryCheckBox = QtWidgets.QCheckBox('Subdirectory:', self)
        self.OperationApplyButton = QtWidgets.QPushButton('Delete files', self)
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
        self.setLayout(vbox)

        self._connect_ui()

    def _connect_ui(self):
        super(DeleteTab, self)._connect_ui()
        self.OperationApplyButton.clicked.connect(self._delete_files)

    def _delete_files(self):
        # Add dialog box to confirm?
        #        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        #        buttonBox.show()
        files_list = self.get_files_lists()[0]
        function = os.remove
        self.run_threaded_process(files_list, function) 