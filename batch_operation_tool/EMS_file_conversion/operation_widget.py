# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 17:16:09 2015

@author: eric
"""
from qtpy import QtWidgets

from batch_operation_tool.EMS_file_conversion.ems_reader import EMSReader


class EMSConversionWidget(QtWidgets.QWidget):

    def __init__(self, get_files_list, parent=None):
        super(EMSConversionWidget, self).__init__(parent=parent)

        self.get_files_list = get_files_list
        self._init_widget()
        self._init_parameters()

    def _init_widget(self):
        self.operation_groupBox = self._create_operation_groupBox()

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.operation_groupBox)
        self.setLayout(vbox)

    def _init_parameters(self):
        self.parameters = {'extension_list': [],
                           'data_type': 'image',
                           'log_to_linear_scale': True,
                           'overwrite': False}

    def _create_operation_groupBox(self):
        groupBox = QtWidgets.QGroupBox("EMS file conversion")

        label1 = QtWidgets.QLabel('Convert to:', self)
        self.extensionconvertionLineEdit = QtWidgets.QLineEdit(self)
        self.overwriteCheckBox = QtWidgets.QCheckBox('Overwrite', self)
        self.radio1 = QtWidgets.QRadioButton("Image")
        self.radio2 = QtWidgets.QRadioButton("Wave function")
        self.LoglinearscaleCheckBox = QtWidgets.QCheckBox(
            'Log to linear scale', self)
        self.radio1.setChecked(True)

        OperationLayout = QtWidgets.QGridLayout()
        # 1st column
        OperationLayout.addWidget(label1, 0, 0)
        OperationLayout.addWidget(self.radio1, 1, 0)
        # 2nd column
        OperationLayout.addWidget(self.extensionconvertionLineEdit, 0, 1)
        OperationLayout.addWidget(self.overwriteCheckBox, 0, 2)
        OperationLayout.addWidget(self.radio2, 1, 1)
        OperationLayout.addWidget(self.LoglinearscaleCheckBox, 1, 2)
        groupBox.setLayout(OperationLayout)

        return groupBox

    def set_parameters(self, extension_list=None, overwrite=None,
                       data_type=None, log_to_linear_scale=None):
        if extension_list is not None:
            self.extensionconvertionLineEdit.setText(', '.join(extension_list))
        if overwrite is not None:
            self.overwriteCheckBox.setChecked(overwrite)
        if data_type is not None:
            if data_type == 'image':
                self.radio1.setChecked(True)
            elif data_type == 'wavefunction':
                self.radio2.setChecked(True)
        if log_to_linear_scale is not None:
            self.LoglinearscaleCheckBox.setChecked(log_to_linear_scale)

    def get_parameters(self):
        self.parameters[
            'extension_list'] = self.extensionconvertionLineEdit.text().split(', ')
        self.parameters['overwrite'] = self.overwriteCheckBox.isChecked()
        if self.radio1.isChecked():
            self.parameters['data_type'] = 'image'
        else:
            self.parameters['data_type'] = 'wavefunction'
        self.parameters[
            'log_to_linear_scale'] = self.LoglinearscaleCheckBox.isChecked()
        return self.parameters

    def convert_file(self):
        files_list = self.get_files_list()[0]
        ems_reader = EMSReader(**self.get_parameters())
        for fname in files_list:
            ems_reader.read(fname)
            ems_reader.convert_ems()
