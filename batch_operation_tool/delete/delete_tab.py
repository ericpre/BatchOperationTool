# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 16:59:12 2015

@author: eric
"""
import os

from batch_operation_tool.base_tab.base_tab import BaseTab


class DeleteTab(BaseTab):

    def __init__(self, fill_tables, parent=None, name="Delete files"):
        """ Need to pass the fill_tables method from parent class"""
        BaseTab.__init__(self, fill_tables=fill_tables, parent=parent)
        self.name = name

    def _initUI(self):
        self._init_baseUI()
        self.OperationApplyButton.setText('Delete')

        self.setLayout(self.vbox)

        self._connect_ui()

    def _connect_ui(self):
        super()._connect_ui()
        self.OperationApplyButton.clicked.connect(self._delete_files)

    def _delete_files(self):
        # Add dialog box to confirm?
        #        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        #        buttonBox.show()
        files_list = self.get_files_lists()[0]
        function = os.remove
        self.run_threaded_process(files_list, function)