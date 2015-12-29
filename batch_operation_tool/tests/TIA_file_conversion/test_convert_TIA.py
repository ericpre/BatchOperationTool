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

    def test_convert_tia_overwrite(self):
        self.tia_reader.overwrite = True
        self.tia_reader.read(self._get_absolute_path(self.tia_reader.fname))
        self.tia_reader.convert_tia()
        assert os.path.exists(self.tia_reader.fname_ext)
        os.remove(self.tia_reader.fname_ext)

    def test_ask_confirmation_overwrite(self):
        item = hs.signals.Image(np.ones((100,100)))
        extension = self.tia_reader.extension_list[0]
        self.tia_reader.set_fname(os.path.join(os.path.dirname(__file__), self.tia_reader.fname))
        self.tia_reader.fname_ext = '.'.join([os.path.splitext(self.tia_reader.fname)[0], extension])
        result = self.tia_reader._ask_confirmation_overwrite(item)
        if result:
            assert os.path.exists(self.tia_reader.fname_ext)
            os.remove(self.tia_reader.fname_ext)
        else:
            assert result == False