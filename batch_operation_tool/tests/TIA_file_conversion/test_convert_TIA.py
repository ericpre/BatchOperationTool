# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 17:26:46 2015

@author: eric
"""
import os, sys
import numpy as np
from python_qt_binding import QtGui
import hyperspy.api as hs

from batch_operation_tool.TIA_file_conversion.convert_TIA import ConvertTIA

class test_ConvertTIA:  
    @classmethod
    def setup_class(self):
        self.app = QtGui.QApplication(sys.argv)

    @classmethod
    def teardown_class(self):
        self.app.quit()

    def setUp(self):
        self.parameter = {'fname':'CCD Search.emi',
                          'extension_list':['jpg'], 'overwrite':False,
                          'contrast_streching':False, 'saturated_pixels':0.4,
                          'normalise':False}
        self.tia_reader = ConvertTIA(**self.parameter)

    def _get_absolute_path(self, fname):
        return os.path.join(os.path.dirname(__file__), fname)

    def test_read(self):
        self.tia_reader.read(self._get_absolute_path(self.tia_reader.fname))
        assert isinstance(self.tia_reader.s, hs.signals.Signal)

    def test_set_fname(self):
        fname = 'dummy_name.ems'
        self.tia_reader.set_fname(fname)
        assert self.tia_reader.fname == fname

    def test_convert_tia_single_item(self):
        self.tia_reader.contrast_streching = True
        self.tia_reader.overwrite = True
        data = np.arange(100).reshape((10,10)).astype("float")
        self.tia_reader._convert_tia_single_item(hs.signals.Image(data))
        assert os.path.exists(self.tia_reader.fname_ext)
        os.remove(self.tia_reader.fname_ext)

        self.tia_reader.contrast_streching = False
        data = np.arange(100).reshape((10,10)).astype("float")
        self.tia_reader._convert_tia_single_item(hs.signals.Image(data))
        assert os.path.exists(self.tia_reader.fname_ext)
        a = hs.load(self.tia_reader.fname_ext)
        a.data = data
        os.remove(self.tia_reader.fname_ext)

    def test_convert_tia_overwrite(self):
        self.tia_reader.overwrite = True
        self.tia_reader.read(self._get_absolute_path(self.tia_reader.fname))
        self.tia_reader.convert_tia()
        assert os.path.exists(self.tia_reader.fname_ext)
        os.remove(self.tia_reader.fname_ext)