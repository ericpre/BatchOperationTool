# -*- coding: utf-8 -*-
# Copyright 2015 Eric Prestat
#
#
# This is a free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# <http://www.gnu.org/licenses/>.-
import os
import numpy as np
import hyperspy.api as hs

from qtpy import QtWidgets
"""
EMS file format: File starts with two 32 bit integers that gives the number of
            	rows and columns of the image. It is followed by the image 
                 data. The data points are Real 4 Bytes (single precision 
                 floating point)
"""


class EMSReader():

    def __init__(self, fname=None, extension_list=['rpl'], overwrite=None,
                 log_to_linear_scale=False, data_type='image'):
        self.fname = fname
        self.extension_list = extension_list
        self.overwrite = overwrite
        self.log_to_linear_scale = log_to_linear_scale
        self.data_type = data_type
        # to ask to overwrite the first time when the checkBox is unchecked
        if not overwrite:
            self.overwrite = None

    def set_fname(self, fname):
        self.fname = fname

    def open_jems_wavefuntion(self, fname):
        with open(fname) as f:
            rows = np.fromfile(f, dtype=np.int32, count=1).newbyteorder('>')[0]
            columns = np.fromfile(f, dtype=np.int32, count=1).newbyteorder('>')[0]
            real_part = np.fromfile(
                f, dtype=np.float32, count=rows * columns).newbyteorder('>').reshape((rows, columns))
            f.read(4)
            imag_part = np.fromfile(
                f, dtype=np.float32, count=rows * columns).newbyteorder('>').reshape((rows, columns))

        return real_part, imag_part

    def open_jems_single_image(self, fname):
        with open(fname) as f:
            rows = np.fromfile(f, dtype=np.int32, count=1).newbyteorder('>')[0]
            columns = np.fromfile(f, dtype=np.int32, count=1).newbyteorder('>')[0]
            ima = np.fromfile(f, dtype=np.float32, count=rows *
                              columns).newbyteorder('>').reshape((rows, columns))

        return ima

    def norm(self, arr, mini=0, maxi=1):
        return (arr - mini) / (maxi - mini)

    def read(self, fname):
        if fname is None:
            fname = self.fname
        else:
            self.fname = fname
        if self.data_type == 'image':
            self.ima = self.open_jems_single_image(fname)
        else:
            self.ima = self.open_jems_wavefuntion(fname)

    def convert_ems(self):
        if self.log_to_linear_scale:
            self.ima = np.exp(self.ima)
        for extension in self.extension_list:
            self.fname_ext = '.'.join(
                [os.path.splitext(self.fname)[0], extension])
            if os.path.exists(self.fname_ext) and self.overwrite is None:
                write_answer = self._ask_confirmation_overwrite()
                self._save_data(overwrite=write_answer)
            else:
                self._save_data(overwrite=self.overwrite)

    def _questionBox(self, fname, path):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle("Overwriting File?")
        question = "Do you want to overwrite the file\n'%s' \nin the folder '%s'?" % (
            fname, path)
        msgBox.setText(question)
        msgBox.addButton(QtWidgets.QMessageBox.Yes)
        msgBox.addButton(QtWidgets.QMessageBox.YesToAll)
        msgBox.addButton(QtWidgets.QMessageBox.No)
        msgBox.addButton(QtWidgets.QMessageBox.NoToAll)
        return msgBox.exec_()

    def _ask_confirmation_overwrite(self):
        # Add a button to ask "Yes to all", "No to all"
        path = os.path.split(self.fname_ext)[0]
        fname = os.path.split(self.fname_ext)[1]
        questionBox = self._questionBox(fname, path)
        if questionBox == QtWidgets.QMessageBox.Yes:
            self.overwrite = None
            return True
        elif questionBox == QtWidgets.QMessageBox.YesToAll:
            self.overwrite = True
            return True
        elif questionBox == QtWidgets.QMessageBox.NoToAll:
            self.overwrite = False
            return False
        else:
            self.overwrite = None
            return False

    def _save_data(self, overwrite=None):
        ima_hs = hs.signals.Signal2D(self.ima)
        ima_hs.save(self.fname_ext, overwrite=overwrite)

if __name__ == '__main__':
    filepath = __file__
    dirname = os.path.dirname
    path = os.path.join(dirname(dirname(filepath)), 'tests',
                        'EMS_conversion')
    fname = os.path.join(path, 'BP-1x3x1-slice_y_0001-thickness0.388nm.ems')
    param = {'fname': fname, 'extension_list': ['rpl'], 'overwrite': False,
             'log_to_linear_scale': False, 'data_type': 'image'}

    ems_reader = EMSReader(**param)
    ems_reader.read(fname)

    import matplotlib.pyplot as plt

    norm_display = 10000
    diff_linear = np.exp(ems_reader.ima)
    plt.figure()
    plt.imshow(diff_linear, vmax=diff_linear.max() / norm_display)
    plt.colorbar()

    question = "Are you sure you want to exit the program?"
    questionBox = QtWidgets.QMessageBox.question(None, 'Overwriting File?',
                                                 question,
                                                 QtWidgets.QMessageBox.Yes,
                                                 QtWidgets.QMessageBox.No)
