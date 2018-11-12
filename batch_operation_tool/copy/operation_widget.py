# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 15:04:58 2015

@author: eric
"""
from qtpy import QtWidgets

from batch_operation_tool.copy.copy import copy_files


class CopyWidget(QtWidgets.QWidget):

    def __init__(self, get_files_list, parent=None):
        super(CopyWidget, self).__init__(parent=parent)

        self.get_files_list = get_files_list
        self._init_widget()
        self._init_parameters()

    def _init_widget(self):
        self.operation_groupBox = self._create_operation_groupBox()

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.operation_groupBox)
        self.setLayout(vbox)

    def _init_parameters(self):
        self.parameters = {'dest_dir': '',
                           'keep_original': True}

    def _create_operation_groupBox(self):
        groupBox = QtWidgets.QGroupBox("Copy")

        label1 = QtWidgets.QLabel('Destination directory:', self)
        self.destdirLineEdit = QtWidgets.QLineEdit(self)
        self.keeporiginalCheckBox = QtWidgets.QCheckBox('Keep original', self)

        OperationLayout = QtWidgets.QGridLayout()
        # 1st column
        OperationLayout.addWidget(label1, 0, 0)
        OperationLayout.addWidget(self.keeporiginalCheckBox, 1, 0)
        # 2nd column
        OperationLayout.addWidget(self.destdirLineEdit, 0, 1)

        groupBox.setLayout(OperationLayout)

        return groupBox

    def set_parameters(self, dest_dir=None, keep_original=None):
        if dest_dir is not None:
            self.destdirLineEdit.setText(dest_dir)
        if keep_original is not None:
            self.keeporiginalCheckBox.setChecked(keep_original)

    def get_parameters(self):
        self.parameters['dest_dir'] = self.destdirLineEdit.text()
        self.parameters[
            'keep_original'] = self.keeporiginalCheckBox.isChecked()
        return self.parameters

    def copy_files(self):
        self.get_parameters()
        files_list = self.get_files_list()[0]
        copy_files(files_list, **self.get_parameters())
