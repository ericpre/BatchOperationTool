#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 22:46:29 2017

@author: eric
"""
import os
import numpy as np
import numpy.testing as nt

from batch_operation_tool.uSTEM_conversion.convert_uSTEM import ConvertuSTEM


path = os.path.dirname(__file__)


def test_read_bin_file():
    filename = 'Ge3Mn5_20nm_DiffPlaneTotal_Detector02_Interpolated_70x120.bin'
    data_object = ConvertuSTEM(os.path.join(path, filename))
    data_object.read()
    nt.assert_array_equal(data_object.s.data,
                          np.load(os.path.join(path, 'STEM_image.npy')))
    