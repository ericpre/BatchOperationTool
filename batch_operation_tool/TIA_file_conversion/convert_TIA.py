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


class ConvertTIA:
    ureg = UnitRegistry()

    def __init__(self, fname=None, extension_list=['tif'], overwrite=None,
                 use_subfolder=True, correct_cfeg_fluctuation=False,
                 add_scalebar=True, contrast_streching=False,
                 saturated_pixels=0.4, normalise=False):
        self.fname = fname
        self.extension_list = extension_list
        self.overwrite = overwrite
        self.use_subfolder = use_subfolder
        self.correct_cfeg_fluctuation = correct_cfeg_fluctuation
        self.add_scalebar = add_scalebar
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
            if extension in ['jpg', 'jpeg'] and self.contrast_streching:
                if isinstance(item, hs.signals.Signal1D):
                    return
                vmin, vmax = contrast_stretching(
                    item.data,
                    f"{self.saturated_pixels/2}th",
                    f'{100-self.saturated_pixels/2}th'
                    )
                item.data = self.stretch_contrast(item.data, vmin, vmax)
                item.data = self.normalise(item.data)
                item.data *= np.iinfo(np.uint8).max
                item.change_dtype(np.uint8)
            if extension in ['tif', 'tiff']:
                if isinstance(item, hs.signals.Signal1D):
                    return
                self._set_convenient_scale(item)
                if self.normalisation:
                    # dirty workaround to read tif file in imagej and dm...
                    item.data = self.normalise(item.data)
                    item.data *= np.iinfo(np.int32).max
                    item.change_dtype(np.int32)
            dname, fname = os.path.split(self.fname)
            if self.use_subfolder:
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
        return msgBox.exec_()

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

    def _save_with_scalebar(self, signal, axes):
        # upstream this part to hyperspy
        from matplotlib_scalebar.scalebar import ScaleBar
        from matplotlib.figure import Figure

        data = signal.data
        dpi = 100
        fig = Figure(figsize=[v/dpi for v in data.shape], dpi=dpi)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        ax.imshow(data, cmap='gray')

        if not isinstance(axes[0].units, str):
            raise ValueError("Units of the signal axis needs to be of string type.")
        scalebar = ScaleBar(axes[0].scale, axes[0].units, box_alpha=0.75,
                            length_fraction=0.4, location='lower left',
                            font_properties={'size':40})
        ax.add_artist(scalebar)
        fig.savefig(self.fullfname, dpi=dpi)

    def _save_data(self, item, overwrite=None, **kwargs):
        try:
            extension = os.path.splitext(self.fullfname)[1]
            if self.add_scalebar and extension in ['.jpg', '.jpeg']:
                try:
                    if len(item.axes_manager.signal_axes) == 2:
                        axes = item.axes_manager.signal_axes
                    elif len(item.axes_manager.navigation_axes) == 2:
                        # Try to use navigation axes
                        axes = item.axes_manager.navigation_axes
                    else:
                        raise ValueError("Data not compatible with saving "
                                         "scale bar.")
                    self._save_with_scalebar(item, axes)

                except ValueError:
                    item.save(self.fullfname, overwrite=overwrite, **kwargs)
            else:
                item.save(self.fullfname, overwrite=overwrite, **kwargs)
        except IOError:
            # In case the format is not supported, fall back to hspy format
            # Add an option to do that
            fname = os.path.splitext(self.fullfname)
            item.save(f'{fname[0]}.hspy', overwrite=overwrite, **kwargs)

    def stretch_contrast(self, arr, vmin, vmax):
        arr[np.where(arr<vmin)] = vmin
        arr[np.where(arr>vmax)] = vmax
        return arr

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
