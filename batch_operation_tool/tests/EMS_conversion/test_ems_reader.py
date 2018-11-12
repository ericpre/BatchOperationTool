# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 00:03:05 2015

@author: eric
"""
import os, sys
import numpy as np
from qtpy import QtWidgets

from batch_operation_tool.EMS_conversion.ems_reader import EMSReader

class Test_EMS_Reader:  
    @classmethod
    def setup_class(self):
        self.app = QtWidgets.QApplication(sys.argv)

    @classmethod
    def teardown_class(self):
        self.app.quit()

    def setup_method(self):
        self.parameter = {'fname':'BP-1x3x1-slice_y_0001-thickness0.388nm.ems',
                          'extension_list':['hdf5'], 'overwrite':False,
                          'log_to_linear_scale':False, 'data_type':'image'}
        self.ems_reader = EMSReader(**self.parameter)
        
    def test_set_fname(self):
        fname = 'dummy_name.ems'
        self.ems_reader.set_fname(fname)
        assert self.ems_reader.fname == fname
        
    def test_open_jems_wavefuntion(self):
        pass
    
    def test_open_jems_single_image(self):
        path = os.path.dirname(__file__)
        fname = os.path.join(path, self.ems_reader.fname)
        ima = self.ems_reader.open_jems_single_image(fname)
        assert isinstance(ima, np.ndarray)

    def test_ask_confirmation_overwrite_yes(self):
        self.ems_reader.ima = np.ones((100,100))
        extension = self.ems_reader.extension_list[0]
        self.ems_reader.set_fname(os.path.join(os.path.dirname(__file__), self.ems_reader.fname))
        self.ems_reader.fname_ext = '.'.join([os.path.splitext(self.ems_reader.fname)[0], extension])
        result = self.ems_reader._ask_confirmation_overwrite()
        if result:
            assert os.path.exists(self.ems_reader.fname_ext)
            os.remove(self.ems_reader.fname_ext)
        else:
            assert result == False

if __name__ == '__main__':
    import pytest
    pytest.main()