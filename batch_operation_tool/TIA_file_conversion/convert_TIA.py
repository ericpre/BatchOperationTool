# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 11:09:50 2015

@author: eric
"""
import os

from qtpy import QtWidgets
from pint import UnitRegistry
import traits.api as t
import numpy as np
import hyperspy.api as hs
from hyperspy.drawing.utils import contrast_stretching
import skimage as ski


class ConvertTIA:
    ureg = UnitRegistry()

    def __init__(self, fname=None, extension_list=['tif'], overwrite=None,
                 use_subfolder=True, correct_cfeg_fluctuation=False,
                 add_scalebar=True, output_size=None, contrast_streching=False,
                 saturated_pixels=0.4, normalise=False, gamma=False,
                 gamma_correction=0.5):
        self.fname = fname
        self.extension_list = extension_list
        self.overwrite = overwrite
        self.use_subfolder = use_subfolder
        self.correct_cfeg_fluctuation = correct_cfeg_fluctuation
        self.add_scalebar = add_scalebar
        if output_size is not None:
            output_size = [s for s in output_size if len(s)]
            if output_size:
                if len(output_size) == 1:
                    output_size = int(output_size[0])
                else:
                    output_size = np.array(output_size, dtype=int)
        self.output_size = output_size if np.any(output_size) else None
        self.contrast_streching = contrast_streching
        self.saturated_pixels = saturated_pixels
        self.normalisation = normalise
        self.gamma_correction = gamma_correction
        self.gamma= gamma
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

    @property
    def is_velox_emd(self):
        if os.path.splitext(self.fname)[1] == '.emd':
            return True
        else:
            return False

    def convert_tia(self):
        if isinstance(self.s, list):
            for i, item in enumerate(self.s):
                suffix = item.metadata.General.title + f"_{i}" if self.is_velox_emd else i
                self._convert_tia_single_item(item, f'_{suffix}')
        else:
            self._convert_tia_single_item(self.s)

    def _convert_tia_single_item(self, item, suffix=''):
        if self.correct_cfeg_fluctuation:
            item = correct_intensity(item)
        original_data = item.data.copy()
        for extension in self.extension_list:
            item.data = original_data
            if extension in ['jpg', 'jpeg']:
                is_rgbx = item.is_rgbx
                if is_rgbx:
                    item.change_dtype(item.data.dtype[0])
                elif isinstance(item, hs.signals.Signal1D):
                    return
                if self.gamma_correction:
                    item.data = self.apply_gamma_correction(item.data)
                if self.contrast_streching:
                    item.data = self.stretch_contrast(item.data)
                item.data = self.normalise(item.data)
                item.data *= np.iinfo(np.uint8).max
                item.change_dtype(np.uint8)
                if is_rgbx:
                    item.change_dtype("rgb8")
            if extension in ['tif', 'tiff']:
                if isinstance(item, hs.signals.Signal1D):
                    return
                try:
                    # TODO: improve this
                    self._set_convenient_scale(item)
                except:
                    pass
                if self.normalisation:
                    # dirty workaround to read tif file in imagej and dm...
                    item.data = self.normalise(item.data)
                    item.data *= np.iinfo(np.int32).max
                    item.change_dtype(np.int32)
            dname, fname = os.path.split(self.fname)
            if self.use_subfolder and self.add_scalebar:
                dname = os.path.join(dname, extension + "-scalebar")
            elif self.use_subfolder:
                dname = os.path.join(dname, extension)
            fname = os.path.join(dname, os.path.splitext(fname)[0])
            self.fullfname = f'{fname}{suffix}.{extension}'
            if os.path.exists(self.fullfname) and self.overwrite is None:
                write_answer = self._ask_confirmation_overwrite()
                self._save_data(item, overwrite=write_answer)
            # workaround, currently hyperspy doesn't write file is
            # overwrite=False
            elif not os.path.exists(self.fullfname):
                self._save_data(item)
            else:
                self._save_data(item, overwrite=self.overwrite)

    def _set_convenient_scale(self, item):
        scale, unit = self._get_scale_unit(item)
        item.axes_manager['x'].scale = scale
        item.axes_manager['y'].scale = scale
        item.axes_manager['x'].units = unit
        item.axes_manager['y'].units = unit

    def _get_scale_unit(self, item):
        unit = item.axes_manager['x'].units
        if unit == t.Undefined:
            # do nothing
            return item.axes_manager['x'].scale, item.axes_manager['x'].units
        if unit == '\xb5m':
            unit = 'um'
#        # workaround for some of the TIA files...
#        # Assuming the <undefined> correspond to TIA files, i. e. the units is 'm'
#        if unit == '<undefined>':
#            unit = 'm'
        scale_u = item.axes_manager['x'].scale * self.ureg(unit)
        scale, unit = self._get_convenient_scale_unit(scale_u)
        return scale, unit

    def _get_convenient_scale_unit(self, scale):
        if scale.dimensionality['[length]'] == 1.0:
            scale = scale.to(self.ureg('m'))
            if scale.magnitude < 1E-9:
                scale = scale.to(self.ureg('nm'))
            elif scale.magnitude < 1E-6:
                scale = scale.to(self.ureg('um'))
            else:
                scale = scale.to(self.ureg('mm'))
            return scale.magnitude, '{}'.format(scale.units)
        elif scale.dimensionality['[length]'] == -1.0:  # for diffraction
            scale = scale.to(self.ureg('1/m'))
            if scale.magnitude > 1E6:
                scale = scale.to(self.ureg('1/nm'))
            elif scale.magnitude > 1E3:
                scale = scale.to(self.ureg('1/um'))
            else:
                scale = scale.to(self.ureg('1/mm'))
            return scale.magnitude, f'{scale.units}'
        else:
            print("Units not supported")
            return scale.magnitude, f'{scale.units}'

    def _questionBox(self, fname, path):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle("Overwriting File?")
        question = f"Do you want to overwrite the file\n'{fname}' \nin the folder '{path}'?"
        msgBox.setText(question)
        msgBox.addButton(QtWidgets.QMessageBox.Yes)
        msgBox.addButton(QtWidgets.QMessageBox.YesToAll)
        msgBox.addButton(QtWidgets.QMessageBox.No)
        msgBox.addButton(QtWidgets.QMessageBox.NoToAll)
        return msgBox.exec()

    def _ask_confirmation_overwrite(self):
        # Add a button to ask "Yes to all", "No to all"
        path, fname = os.path.split(self.fullfname)
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

    def _save_data(self, item, overwrite=None, **kwargs):
        try:
            extension = os.path.splitext(self.fullfname)[1]
            if (item.axes_manager.signal_dimension == 0 and
                item.axes_manager.navigation_dimension == 2):
                item = item.T

            if ((self.add_scalebar or np.any(self.output_size) is not None) and
                extension in ['.jpg', '.jpeg']):
                try:
                    if len(item.axes_manager.signal_axes) != 2:
                        raise ValueError("Data not compatible with saving "
                                         "scale bar.")
                    kwargs = dict(
                        scalebar=self.add_scalebar, output_size=self.output_size
                        )
                    item.save(self.fullfname, overwrite=overwrite, **kwargs)

                except ValueError:
                    item.save(self.fullfname, overwrite=overwrite, **kwargs)
            else:
                item.save(self.fullfname, overwrite=overwrite, **kwargs)
        except IOError:
            # In case the format is not supported, fall back to hspy format
            # Add an option to do that
            fname = os.path.splitext(self.fullfname)
            item.save(f'{fname[0]}.hspy', overwrite=overwrite, **kwargs)

    def stretch_contrast(self, arr):
        saturation = self.saturated_pixels
        vmin, vmax = contrast_stretching(
            arr, f"{saturation/2}th", f'{100-saturation/2}th'
            )
        arr[np.where(arr<vmin)] = vmin
        arr[np.where(arr>vmax)] = vmax
        return arr

    def apply_gamma_correction(self, arr):
        return ski.exposure.adjust_gamma(arr, gamma=self.gamma)

    def normalise(self, arr, vmin=None, vmax=None):
        if vmin == None:
            vmin = arr.min()
        if vmax == None:
            vmax = arr.max()
        return (arr.astype(float) - vmin) / (vmax - vmin)


def correct_intensity(signal, axis=-2):
    before_mean = signal.data.mean()
    signal.data = signal.data / signal.mean(axis).data[..., np.newaxis]
    after_mean = signal.data.mean()
    return signal * before_mean / after_mean


if __name__ == '__main__':
    fname = '10.51.36 Scanning Acquire.emi'
    convert_TIA_file = ConvertTIA(overwrite=True)

    s = hs.load(fname)
    convert_TIA_file.read(fname)
    convert_TIA_file.convert_tia()
