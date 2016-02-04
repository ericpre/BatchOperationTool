# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 11:09:50 2015

@author: eric
"""
import os
from python_qt_binding import QtGui

import hyperspy.api as hs
from hyperspy.misc.image_tools import contrast_stretching

class ConvertTIA:
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
        """ An attempt to add the scale in tif file to be read in ImageJ: not working... 
        if ext == 'tif':
            scale = ima.axes_manager[0].scale
            if unit is None:
                unit = ima.axes_manager[0].units
            if unit == 'nm':
                scale = scale*np.power(10, 9)
            if unit == u'\xb5m':
                scale = scale*np.power(10, 6)
            print scale
            kwargs['resolution'] = [json.dumps(scale), json.dumps(scale)]
            vmin, vmax = contrast_stretching(image.data, saturated_pixels)
            kwargs['description'] = json.dumps('ImageJ=1.49v unit=nm min=%.3f max=%.3f'%(vmin, vmax))
        """
        if self.contrast_streching:
            vmin, vmax = contrast_stretching(item.data, self.saturated_pixels)
            item.data = self.normalise(item.data, vmin, vmax)
        for extension in self.extension_list:
            self.fname_ext = ''.join([os.path.splitext(self.fname)[0], suffix,
                                      '.', extension])
            if os.path.exists(self.fname_ext) and self.overwrite is None:
                write_answer = self._ask_confirmation_overwrite()
                self._save_data(item, overwrite=write_answer)
            else:
                self._save_data(item, overwrite=self.overwrite)

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

    def _save_data(self, item, overwrite=None):
        item.save(self.fname_ext, overwrite=overwrite)

    def normalise(self, arr, vmin=None, vmax=None):
        if vmin == None:
            vmin = arr.min()
        if vmax == None:
            vmax = arr.max()
        return (arr.astype(float)-vmin)/(vmax-vmin)

if __name__ == '__main__':        
    fname = '12.37.10 CCD Acquire.emi'
    convert_TIA_file = ConvertTIA()    
    
    s = hs.load(fname)
    for ima in s:
        convert_TIA_file.export_image(ima, unit=None, ext='tif')
