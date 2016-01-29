# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 15:04:58 2015

@author: eric
"""
from python_qt_binding import QtGui

from batch_operation_tool.TIA_file_conversion.convert_TIA import ConvertTIA

class TIAConversionWidget(QtGui.QWidget):
    def __init__(self, get_files_list, parent=None):
        super(TIAConversionWidget, self).__init__(parent=parent)

        self.get_files_list = get_files_list
        self._init_widget()
        self._init_parameters()
        
    def _init_widget(self):                      
        self.operation_groupBox = self._create_operation_groupBox()

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.operation_groupBox)
        self.setLayout(vbox)

    def _init_parameters(self):
        self.parameters = {'extension_list':[],
                           'overwrite':False,
                           'contrast_streching':True,
                           'saturated_pixels':0.4,
                           'normalise':False}

    def _create_operation_groupBox(self):
        groupBox = QtGui.QGroupBox("TIA file conversion")

        label1 = QtGui.QLabel('Convert to:', self)
        self.extensionconvertionLineEdit = QtGui.QLineEdit(self)
        self.overwriteCheckBox = QtGui.QCheckBox('Overwrite', self)
        self.contraststrechingCheckBox = QtGui.QCheckBox('Contrast streching', self)
        self.saturatedpixelsLineEdit = QtGui.QLineEdit(self)
        self.normaliseCheckBox = QtGui.QCheckBox('Normalise', self)

        OperationLayout = QtGui.QGridLayout()
        # 1st column
        OperationLayout.addWidget(label1, 0, 0)
        OperationLayout.addWidget(self.contraststrechingCheckBox, 1, 0)
        # 2nd column        
        OperationLayout.addWidget(self.extensionconvertionLineEdit, 0, 1)
        OperationLayout.addWidget(self.saturatedpixelsLineEdit, 1, 1)
        # 3td column
        OperationLayout.addWidget(self.overwriteCheckBox, 0, 2)
        OperationLayout.addWidget(self.normaliseCheckBox, 1, 2)
        groupBox.setLayout(OperationLayout)
      
        return groupBox
        
    def set_parameters(self, extension_list=None, overwrite=None,
                       contrast_streching=None, saturated_pixels=None,
                       normalise=None):
        if extension_list is not None:
            self.extensionconvertionLineEdit.setText(', '.join(extension_list))
        if overwrite is not None:
            self.overwriteCheckBox.setChecked(overwrite)
        if contrast_streching is not None:
            self.contraststrechingCheckBox.setChecked(contrast_streching)
        if saturated_pixels is not None:
            self.saturatedpixelsLineEdit.setText(str(saturated_pixels))
        if normalise is not None:
            self.normaliseCheckBox.setChecked(normalise)            
            
    def get_parameters(self):
        self.parameters['extension_list'] = self.extensionconvertionLineEdit.text().split(', ')
        self.parameters['overwrite'] = self.overwriteCheckBox.isChecked()
        self.parameters['contrast_streching'] = self.contraststrechingCheckBox.isChecked()
        self.parameters['saturated_pixels'] = float(self.saturatedpixelsLineEdit.text())
        self.parameters['normalise'] = self.normaliseCheckBox.isChecked()
        return self.parameters
        
    def convert_file(self):
        files_list = self.get_files_list()[0]
        convert_tia = ConvertTIA(**self.get_parameters())
        for fname in files_list:
            convert_tia.read(fname)
            result = convert_tia.convert_tia()
            if result == 'NoToAll':
                break