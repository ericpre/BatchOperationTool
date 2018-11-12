# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 15:04:58 2015

@author: eric
"""
from qtpy import QtWidgets
import numpy as np
import hyperspy.api as hs

from batch_operation_tool.uSTEM_conversion.convert_uSTEM import ConvertuSTEM


class uSTEMConversionWidget(QtWidgets.QWidget):

    def __init__(self, get_files_list, parent=None):
        super(uSTEMConversionWidget, self).__init__(parent=parent)

        self.get_files_list = get_files_list
        self._init_widget()
        self._init_parameters()

    def _init_widget(self):
        self.operation_groupBox = self._create_operation_groupBox()
        
        # TODO: add support for `save_as_stack`, disable it in the mean time
        self.savestackCheckBox.hide()

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.operation_groupBox)
        self.setLayout(vbox)

    def _init_parameters(self):
        self.parameters = {'extension_list': [],
                           'overwrite': False,
                           'contrast_streching': True,
                           'saturated_pixels': 0.4,
                           'normalise': False,
                           'save_stack': True}

    def _create_operation_groupBox(self):
        groupBox = QtWidgets.QGroupBox("bin file conversion")

        label1 = QtWidgets.QLabel('Convert to:', self)
        self.extensionconvertionLineEdit = QtWidgets.QLineEdit(self)
        self.overwriteCheckBox = QtWidgets.QCheckBox('Overwrite', self)
        self.contraststrechingCheckBox = QtWidgets.QCheckBox(
            'Contrast streching', self)
        self.saturatedpixelsLineEdit = QtWidgets.QLineEdit(self)
        self.normaliseCheckBox = QtWidgets.QCheckBox('Normalise', self)
        self.savestackCheckBox = QtWidgets.QCheckBox('Save Stack', self)

        OperationLayout = QtWidgets.QGridLayout()
        # 1st column
        OperationLayout.addWidget(label1, 0, 0)
        OperationLayout.addWidget(self.contraststrechingCheckBox, 1, 0)
        # 2nd column
        OperationLayout.addWidget(self.extensionconvertionLineEdit, 0, 1)
        OperationLayout.addWidget(self.saturatedpixelsLineEdit, 1, 1)
        # 3td column
        OperationLayout.addWidget(self.overwriteCheckBox, 0, 2)
        OperationLayout.addWidget(self.normaliseCheckBox, 1, 2)
        OperationLayout.addWidget(self.savestackCheckBox, 2, 1)
        groupBox.setLayout(OperationLayout)

        return groupBox

    def set_parameters(self, extension_list=None, overwrite=None,
                       contrast_streching=None, saturated_pixels=None,
                       normalise=None, save_stack=None):
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
        if save_stack is not None:
            self.savestackCheckBox.setChecked(save_stack)

    def get_parameters(self):
        self.parameters[
            'extension_list'] = self.extensionconvertionLineEdit.text().split(', ')
        self.parameters['overwrite'] = self.overwriteCheckBox.isChecked()
        self.parameters[
            'contrast_streching'] = self.contraststrechingCheckBox.isChecked()
        self.parameters['saturated_pixels'] = float(
            self.saturatedpixelsLineEdit.text())
        self.parameters['normalise'] = self.normaliseCheckBox.isChecked()
        self.parameters['save_stack'] = self.savestackCheckBox.isChecked()
        return self.parameters

    def _get_keywords_list(self, files_list):
        """
        Absorption model template:
        <Prefix>_Image_<NX>x<NY>.bin
        <Prefix>_DiffractionPattern_<NX>x<NY>.bin
        
        QED model template:
        <Prefix>_DiffPlaneTotal_<NX>x<NY>.bin
        <Prefix>_DiffPlaneElastic_<NX>x<NY>.bin
        <Prefix>_DiffPlaneTDS_<NX>x<NY>.bin
        <Prefix>_ExitSurface_IntensityElastic_<NX>x<NY>.bin
        <Prefix>_ExitSurface_PhaseElastic_<NX>x<NY>.bin
        <Prefix>_ExitSurface_IntensityTotal_<NX>x<NY>.bin
        <Prefix>_ExitSurface_IntensityTDS_<NX>x<NY>.bin
        <Prefix>_Image_Elastic_<NX>x<NY>.bin
        <Prefix>_Image_TDS_<NX>x<NY>.bin
        <Prefix>_Image_Total_<NX>x<NY>.bin
        """

        keywords_list_default = ['Image',
                                 'DiffractionPattern',
                                 'DiffPlaneTotal',
                                 'DiffPlaneElastic',
                                 'DiffPlaneTDS',
                                 'ExitSurface_IntensityElastic',
                                 'ExitSurface_PhaseElastic',
                                 'ExitSurface_IntensityTotal',
                                 'ExitSurface_IntensityTDS',
                                 'Image_Elastic',
                                 'Image_TDS',
                                 'Image_Total']
        
        self.keywords_list = []
        self.stack_dict = {}
        self.stack_size = len(files_list)
        self.stack_index = 0
        for filename in sorted(files_list):
            for keyword in keywords_list_default:
                if keyword in filename:
                    if '_Interpolated_' in filename:
                        keyword = '%s_Interpolated'%keyword
                    if keyword not in self.keywords_list:
                        self.keywords_list.append(keyword)
        print(self.keywords_list)

                    
    def _add_data_to_stack(self, fname, data):
        for keyword in self.keywords_list:
            if keyword in fname:
                if keyword in self.stack_dict.keys():
                    # add to already existing stack
                    self.stack_dict[keyword][self.stack_index] = data
                else:
                    self.stack_dict[keyword] = np.zeros((self.stack_size,
                                                         data.shape[0],
                                                         data.shape[1]))

    def _save_stack(self):
        for keyword in self.keywords_list:
            s = hs.signals.Signal2D(self.stack_dict[keyword])
            s.save('%s.tif'%keyword)

    def _setup_conversion(self):
        self.convert_uSTEM = ConvertuSTEM(**self.get_parameters())

    def convert_file(self, fname):
        # TODO: add support for `save_as_stack`, which means read all images
        self.convert_uSTEM.read(fname)
        self.convert_uSTEM.convert()

    # def convert_file(self):
    #     param = self.get_parameters()
    #     save_stack = param['save_stack']
    #     files_list = self.get_files_list()[0]
    #     convert_bin = ConvertBin(**param)
    #     if save_stack:
    #         self._get_keywords_list(files_list)
    #     for fname in files_list:
    #         convert_bin.read(fname)
    #         convert_bin.convert_bin()
    #         if save_stack:
    #             self._add_data_to_stack(fname, convert_bin.s.data)
    #     if save_stack:
    #         self._save_stack()
