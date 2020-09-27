# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 17:26:46 2015

@author: eric
"""
import os
import numpy as np
import numpy.testing as nt
import hyperspy.api as hs
import pytest

from batch_operation_tool.TIA_file_conversion.convert_TIA import ConvertTIA

class Test_ConvertTIA:
    def setup_method(self):
        self.delete_files = True
        self.parameter = {'fname':'128x128-TEM_search.emi',
                          'extension_list':['jpg'], 'overwrite':False,
                          'use_subfolder': False,
                          'contrast_streching':False, 'saturated_pixels':0.4,
                          'normalise':False}
        self.tia_reader = ConvertTIA(**self.parameter)

    def _get_absolute_path(self, fname):
        return os.path.join(os.path.dirname(__file__), fname)

    def test_read(self):
        self.tia_reader.read(self._get_absolute_path(self.tia_reader.fname))
        assert isinstance(self.tia_reader.s, hs.signals.BaseSignal)

    def test_set_fname(self):
        fname = 'dummy_name.emi'
        self.tia_reader.set_fname(fname)
        assert self.tia_reader.fname == fname

    def test_get_scale_unit(self):
        self.tia_reader.read(self._get_absolute_path(self.tia_reader.fname))
        a = self.tia_reader._get_scale_unit(self.tia_reader.s)
        nt.assert_allclose(a[0], 0.005261, rtol=1e-4)
        assert a[1] == 'micrometer'

    @pytest.mark.parametrize('use_subfolder', [False, True])
    def test_convert_tia_list_extention(self, use_subfolder):
        self.tia_reader.extension_list = ['tif', 'jpg']
        self.tia_reader.read(self._get_absolute_path(self.tia_reader.fname))
        self.tia_reader.use_subfolder = use_subfolder
        self.tia_reader.convert_tia()
        # the last one to be saved is with 'jpg' extension
        fname0 = self.tia_reader.fullfname
        fname1 = fname0.replace('jpg', 'tif')
        assert os.path.exists(fname0)
        assert os.path.exists(fname1)
        print('fname0', fname0)
        print('fname1', fname1)
        if self.delete_files:
            os.remove(fname0)
            os.remove(fname1)

    @pytest.mark.parametrize('use_subfolder', [False, True])
    def test_convert_tia_list_signal(self, use_subfolder):
        fname = '16x16_STEM_BF_DF_acquire.emi'
        self.tia_reader.read(self._get_absolute_path(fname))
        self.tia_reader.use_subfolder = use_subfolder
        self.tia_reader.convert_tia()
        fname1 = self.tia_reader.fullfname
        fname0 = fname1.replace('_1.jpg', '_0.jpg')
        assert os.path.exists(fname0)
        assert os.path.exists(fname1)
        print('fname0', fname0)
        print('fname1', fname1)
        if self.delete_files:
            os.remove(fname0)
            os.remove(fname1)

    def test_convert_tia_single_item(self):
        self.tia_reader.contrast_streching = True
        self.tia_reader.overwrite = True
        data = np.arange(100).reshape((10,10)).astype("float")
        self.tia_reader._convert_tia_single_item(hs.signals.Signal2D(data))
        assert os.path.exists(self.tia_reader.fullfname)
        if self.delete_files:
            os.remove(self.tia_reader.fullfname)

        self.tia_reader.contrast_streching = False
        data = np.arange(100).reshape((10,10)).astype("float")
        self.tia_reader._convert_tia_single_item(hs.signals.Signal2D(data))
        assert os.path.exists(self.tia_reader.fullfname)
        a = hs.load(self.tia_reader.fullfname)
        a.data = data
        if self.delete_files:
            os.remove(self.tia_reader.fullfname)

        self.tia_reader.contrast_streching = False
        self.tia_reader.read(self._get_absolute_path(self.tia_reader.fname))
        self.tia_reader.extension_list = ['tif']
        self.tia_reader._convert_tia_single_item(self.tia_reader.s)
        assert os.path.exists(self.tia_reader.fullfname)
        fname = self._get_absolute_path(self.tia_reader.fname.replace('.emi', ''))
        s = hs.load(fname+'.tif')
        nt.assert_array_equal(s.data, np.load(fname+'.npy'))
        if self.delete_files:
            os.remove(self.tia_reader.fullfname)

    def test_convert_tia_overwrite(self):
        self.tia_reader.overwrite = True
        self.tia_reader.read(self._get_absolute_path(self.tia_reader.fname))
        self.tia_reader.convert_tia()
        assert os.path.exists(self.tia_reader.fullfname)
        if self.delete_files:
            os.remove(self.tia_reader.fullfname)

if __name__ == '__main__':
    import pytest
    pytest.main()