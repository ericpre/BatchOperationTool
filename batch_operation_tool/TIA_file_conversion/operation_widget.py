# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 15:04:58 2015

@author: eric
"""
from qtpy import QtWidgets

from batch_operation_tool.TIA_file_conversion.convert_TIA import ConvertTIA


class TIAConversionWidget(QtWidgets.QWidget):

    def __init__(self, get_files_list, parent=None):
        super(TIAConversionWidget, self).__init__(parent=parent)

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
                           'overwrite': False,
                           'use_subfolder': True,
                           'add_scalebar': True,
                           'correct_cfeg_fluctuation': False,
                           'contrast_streching': True,
                           'saturated_pixels': 0.4,
                           'normalise': True,
                           'gamma_correction': False,
                           'gamma':0.5}

    def _create_operation_groupBox(self):
        groupBox = QtWidgets.QGroupBox("TIA file conversion")

        label1 = QtWidgets.QLabel('Convert to:', self)
        label2 = QtWidgets.QLabel('Output size:', self)
        self.extensionconvertionLineEdit = QtWidgets.QLineEdit(self)
        self.outputsizeLineEdit = QtWidgets.QLineEdit(self)
        self.overwriteCheckBox = QtWidgets.QCheckBox('Overwrite', self)
        self.usesubfolderCheckBox = QtWidgets.QCheckBox('Export to subfolder', self)
        self.addscalebarCheckBox = QtWidgets.QCheckBox('Add scalebar', self)
        self.correctcfegCheckBox = QtWidgets.QCheckBox('Correct CFEG fluctuation', self)
        self.contraststrechingCheckBox = QtWidgets.QCheckBox('Contrast streching', self)
        self.saturatedpixelsLineEdit = QtWidgets.QLineEdit(self)
        self.gammacorrectionCheckBox = QtWidgets.QCheckBox('Gamma Correction', self)
        self.gammaLineEdit = QtWidgets.QLineEdit(self)
        self.normaliseCheckBox = QtWidgets.QCheckBox('Normalise', self)

        OperationLayout = QtWidgets.QGridLayout()
        # 1st column
        OperationLayout.addWidget(label1, 0, 0)
        OperationLayout.addWidget(label2, 1, 0)
        OperationLayout.addWidget(self.contraststrechingCheckBox, 2, 0)
        OperationLayout.addWidget(self.gammacorrectionCheckBox, 3, 0)
        # 2nd column
        OperationLayout.addWidget(self.extensionconvertionLineEdit, 0, 1)
        OperationLayout.addWidget(self.outputsizeLineEdit, 1, 1)
        OperationLayout.addWidget(self.saturatedpixelsLineEdit, 2, 1)
        OperationLayout.addWidget(self.gammaLineEdit, 3, 1)
        # 3td column
        OperationLayout.addWidget(self.overwriteCheckBox, 0, 2)
        OperationLayout.addWidget(self.addscalebarCheckBox, 1, 2)
        OperationLayout.addWidget(self.normaliseCheckBox, 2, 2)
        # 4th column
        OperationLayout.addWidget(self.usesubfolderCheckBox, 0, 3)
        OperationLayout.addWidget(self.correctcfegCheckBox, 2, 3)

        groupBox.setLayout(OperationLayout)

        return groupBox

    def set_parameters(self, extension_list=None, overwrite=None,
                       use_subfolder=None, output_size=None, add_scalebar=None,
                       correct_cfeg_fluctuation=None,
                       contrast_streching=None,
                       saturated_pixels=None, normalise=None,
                       gamma_correction=None, gamma=None):
        if extension_list is not None:
            self.extensionconvertionLineEdit.setText(', '.join(extension_list))
        if overwrite is not None:
            self.overwriteCheckBox.setChecked(overwrite)
        if use_subfolder is not None:
            self.usesubfolderCheckBox.setChecked(use_subfolder)
        if add_scalebar is not None:
            self.addscalebarCheckBox.setChecked(add_scalebar)
        if output_size is not None:
            self.outputsizeLineEdit.setText(', '.join(output_size))
        if correct_cfeg_fluctuation is not None:
            self.correctcfegCheckBox.setChecked(correct_cfeg_fluctuation)
        if contrast_streching is not None:
            self.contraststrechingCheckBox.setChecked(contrast_streching)
        if saturated_pixels is not None:
            self.saturatedpixelsLineEdit.setText(str(saturated_pixels))
        if normalise is not None:
            self.normaliseCheckBox.setChecked(normalise)
        if gamma_correction:
            self.gammacorrectionCheckBox.setChecked(gamma_correction)
        if gamma:
            self.gammaLineEdit.setText(str(gamma))

    def get_parameters(self):
        self.parameters[
            'extension_list'] = self.extensionconvertionLineEdit.text().split(', ')
        self.parameters['overwrite'] = self.overwriteCheckBox.isChecked()
        self.parameters['use_subfolder'] = self.usesubfolderCheckBox.isChecked()
        self.parameters['add_scalebar'] = self.addscalebarCheckBox.isChecked()
        self.parameters['output_size'] = self.outputsizeLineEdit.text().split(', ')
        self.parameters['correct_cfeg_fluctuation'] = self.correctcfegCheckBox.isChecked()
        self.parameters[
            'contrast_streching'] = self.contraststrechingCheckBox.isChecked()
        self.parameters['saturated_pixels'] = float(
            self.saturatedpixelsLineEdit.text())
        self.parameters['normalise'] = self.normaliseCheckBox.isChecked()
        self.parameters[
            'gamma_correction'] = self.gammacorrectionCheckBox.isChecked()
        self.parameters['gamma'] = float(self.gammaLineEdit.text())
        return self.parameters

    def _setup_conversion(self):
        self.convert_tia = ConvertTIA(**self.get_parameters())

    def convert_file(self, fname):
        self.convert_tia.read(fname)
        self.convert_tia.convert_tia()
