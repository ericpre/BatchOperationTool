# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 11:09:50 2015

@author: eric
"""
import os, sys
from python_qt_binding import QtGui
from pint import UnitRegistry

import hyperspy.api as hs
from hyperspy.misc.image_tools import contrast_stretching

class ConvertTIA:
    ureg = UnitRegistry()
    
    def __init__(self, fname=None, extension_list=['jpg'], overwrite=None,
                 contrast_streching=False, saturated_pixels=0.4,
                 normalise=False):
        self.fname = fname
        self.extension_list = extension_list
        self.overwrite = overwrite
        self.contrast_streching = contrast_streching
        self.saturated_pixels = saturated_pixels
        self.normalisation = normalise
        # to ask to overwrite the first time when the checkBox is unchecked
        if not overwrite:
            self.overwrite = None

    def set_fname(self, fname):
        self.fname = fname

    def read(self, fname):
        if fname is None:
            fname = self.fname
        else:
            self.fname = fname
        self.s = hs.load(fname)

    def convert_tia(self):
        if isinstance(self.s, list):
            for i, item in enumerate(self.s):
                suffix = '_'+str(i)
                self._convert_tia_single_item(item, suffix)
        else:
            self._convert_tia_single_item(self.s)
        
    def _convert_tia_single_item(self, item, suffix=''):
        kwargs = {}
        if self.contrast_streching:
            vmin, vmax = contrast_stretching(item.data, self.saturated_pixels)
            item.data = self.normalise(item.data, vmin, vmax)
        for extension in self.extension_list:
            if extension in ['tif', 'tiff']:
                kwargs = self._imagej_kwargs(item)
            self.fname_ext = ''.join([os.path.splitext(self.fname)[0], suffix,
                                      '.', extension])
            if os.path.exists(self.fname_ext) and self.overwrite is None:
                write_answer = self._ask_confirmation_overwrite()
                self._save_data(item, overwrite=write_answer, **kwargs)
            # workaround, currently hyperspy doesn't write file is overwrite=False 
            elif not os.path.exists(self.fname_ext):
                self._save_data(item, **kwargs)
            else:
                self._save_data(item, overwrite=self.overwrite, **kwargs)

    def _imagej_kwargs(self, item, factor=int(1E8)):
        unit = item.axes_manager['x'].units
        if unit == u'\xb5m':
            unit = 'um'
        # workaround for some of the TIA files...
        # Assuming the <undefined> correspond to TIA files, i. e. the units is 'm'
        if unit == '<undefined>':
            unit = 'm'
        print unit
        scale_u = item.axes_manager['x'].scale*self.ureg(unit)
        print scale_u
        scale, unit = self._get_convenient_scale_unit(scale_u)        
        print scale, unit
        resolution = ((factor, int(scale*factor)), (factor, int(scale*factor)))
        description_string = imagej_description(kwargs={"unit":unit})
        extratag = [(270, 's', 1, description_string, False)]
        return {"resolution":resolution, "extratags":extratag}

    def _get_convenient_scale_unit(self, scale):
        if scale.dimensionality['[length]'] == 1.0:
            scale = scale.to(self.ureg('m'))
            if scale.magnitude < 1E-9:
                scale = scale.to(self.ureg('nm'))
            elif scale.magnitude < 1E-6:
                scale = scale.to(self.ureg('um'))
            else:
                scale = scale.to(self.ureg('mm'))
            return scale.magnitude, scale.units
        elif scale.dimensionality['[length]'] == -1.0: # for diffraction
            scale = scale.to(self.ureg('1/m'))
            if scale.magnitude > 1E6:
                scale = scale.to(self.ureg('1/nm'))
            elif scale.magnitude > 1E3:
                scale = scale.to(self.ureg('1/um'))
            else:
                scale = scale.to(self.ureg('1/mm'))
            return scale.magnitude, scale.units
        else:
            print "Units not supported"
            return scale.magnitude, scale.units

    def _questionBox(self, fname, path):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Overwriting File?")
        question = "Do you want to overwrite the file\n'%s' \nin the folder '%s'?"%(fname, path)
        msgBox.setText(question)
        msgBox.addButton(QtGui.QMessageBox.Yes)
        msgBox.addButton(QtGui.QMessageBox.YesToAll)
        msgBox.addButton(QtGui.QMessageBox.No)
        msgBox.addButton(QtGui.QMessageBox.NoToAll)
        return msgBox.exec_()     

    def _ask_confirmation_overwrite(self):
        # Add a button to ask "Yes to all", "No to all"
        path = os.path.split(self.fname_ext)[0]
        fname = os.path.split(self.fname_ext)[1]
        questionBox = self._questionBox(fname, path)
        if questionBox == QtGui.QMessageBox.Yes:
            self.overwrite = None
            return True
        elif questionBox == QtGui.QMessageBox.YesToAll:
            self.overwrite = True
            return True
        elif questionBox == QtGui.QMessageBox.NoToAll:
            self.overwrite = False
            return False
        else:
            self.overwrite = None
            return False

    def _save_data(self, item, overwrite=None, **kwargs):
        item.save(self.fname_ext, overwrite=overwrite, **kwargs)

    def normalise(self, arr, vmin=None, vmax=None):
        if vmin == None:
            vmin = arr.min()
        if vmax == None:
            vmax = arr.max()
        return (arr.astype(float)-vmin)/(vmax-vmin)

if sys.version_info[0] > 2:
    basestring = str, bytes
    unicode = str

    def str2bytes(s, encoding="latin-1"):
        return s.encode(encoding)
else:
    def str2bytes(s):
        return s

def imagej_description(version='1.11a', kwargs={}):
    result = ['ImageJ=%s' % version]
    append = []
    for key, value in kwargs.items():
        append.append('%s=%s' % (key.lower(), value))

    return '\n'.join(result + append + [''])

if __name__ == '__main__':        
    fname = '12.37.10 CCD Acquire.emi'
    convert_TIA_file = ConvertTIA()    
    
    s = hs.load(fname)
    convert_TIA_file.read(fname)
    convert_TIA_file.convert_tia()