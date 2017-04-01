# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 16:59:12 2015

@author: eric
"""
from qtpy import QtWidgets

from batch_operation_tool.base_tab.base_tab import BaseTab
from batch_operation_tool.copy.filter_widget import FilterWidget
from batch_operation_tool.copy.operation_widget import CopyWidget


class CopyTab(BaseTab):

    def __init__(self, fill_tables, parent=None, name="Copy files"):
        """ Need to pass the fill_tables method from parent class"""
        BaseTab.__init__(self, fill_tables=fill_tables, parent=parent)
        self.name = name
#        self._initUI()
#        self._init_main_parameters()
#        self.fill_tables = fill_tables

    def _initUI(self):
        self.filter_widget = FilterWidget(parent=self)
        self.copy_widget = CopyWidget(get_files_list=self.get_files_lists,
                                      parent=self)

        self.SelectFolderButton = QtWidgets.QPushButton('Select folder', self)
        self.SubdirectoryCheckBox = QtWidgets.QCheckBox('Subdirectory:', self)
        self.OperationApplyButton = QtWidgets.QPushButton('Copy files', self)
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
        vbox.addWidget(self.copy_widget)
        self.setLayout(vbox)

        self._connect_ui()
        self._connect_open_folder()

    def _connect_open_folder(self):
        self.SelectFolderButton.clicked.connect(self._set_dest_dit)

    def _set_dest_dit(self):
        self.copy_widget.set_parameters(dest_dir=self.filter_widget.dname)

    def _connect_ui(self):
        super(CopyTab, self)._connect_ui()
        self.OperationApplyButton.clicked.connect(self._copy_files)

    def _copy_files(self):
        # Add dialog box to confirm?
        #        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        #        buttonBox.show()
        self.copy_widget.copy_files()

        self.refresh_table()
