# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 14:32:20 2015

@author: eric
"""

import os
from qtpy import QtWidgets, QtCore
import json

import batch_operation_tool
from batch_operation_tool.progressbar import ThreadedProgressBar
from batch_operation_tool.base_tab.filter_widget_base import FilterWidgetBase


class BaseTab(QtWidgets.QWidget):

    def __init__(self, fill_tables, parent=None):
        """ Need to pass the fill_tables method from parent class"""
        super(BaseTab, self).__init__(parent=parent)
        self._initUI()
        self._init_main_parameters()
        self.fill_tables = fill_tables

    def _init_baseUI(self):

        self.SelectFolderButton = QtWidgets.QPushButton('Select folder', self)
        self.SubdirectoryCheckBox = QtWidgets.QCheckBox('Subdirectory', self)
        self.OperationApplyButton = QtWidgets.QPushButton('Operation', self)
        self.LoadConfigButton = QtWidgets.QPushButton('Load config', self)
        self.SaveConfigButton = QtWidgets.QPushButton('Save config', self)

        current_folder_label = QtWidgets.QLabel( 'Current folder:', self)
        self.current_folderLineEdit = QtWidgets.QLineEdit(self)

        self.filter_widget = FilterWidgetBase(parent=self)

        # layout
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self.SelectFolderButton)
        hbox1.addWidget(self.SubdirectoryCheckBox)
        hbox1.addWidget(self.OperationApplyButton)
        hbox1.addWidget(self.LoadConfigButton)
        hbox1.addWidget(self.SaveConfigButton)
        # need to combine hbox1 into a single widget
        hbox1_widget = QtWidgets.QWidget()
        hbox1_widget.setLayout(hbox1)

        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(current_folder_label)
        hbox2.addWidget(self.current_folderLineEdit)
        hbox2_widget = QtWidgets.QWidget()
        hbox2_widget.setLayout(hbox2)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(hbox1_widget)
        self.vbox.addWidget(hbox2_widget)
        self.vbox.addWidget(self.filter_widget)

    def _initUI(self):
        self._init_baseUI()
        self.setLayout(self.vbox)
        self._connect_ui()

    def _connect_ui(self):
        self.current_folderLineEdit.returnPressed.connect(self._on_valided_current_folder)
        self.SelectFolderButton.clicked.connect(self._open_directory_dialog)
        self.SubdirectoryCheckBox.clicked.connect(self._update_subdirectory)
        self.LoadConfigButton.clicked.connect(self._load_config_dialog)
        self.SaveConfigButton.clicked.connect(self._save_config_dialog)

    def _init_main_parameters(self, subdirectory=False):
        self.main_parameters = {'directory': self.dname,
                                'subdirectory': subdirectory}

    def load_config(self, fname=None):
        if fname is None:
            fname = os.path.join(self._get_library_path(), 'delete',
                                 'default_settings.json')
        with open(fname, "r") as data_file:
            config = json.load(data_file)
        main_parameters = config['Main']
        filter_parameters = config['Filter']
        self._set_main_parameters(**main_parameters)
        self.set_filter_parameters(**filter_parameters)

    def _get_library_path(self):
        return os.path.dirname(batch_operation_tool.__file__)

    def _save_config(self, fname=None):
        if fname is None:
            fname = os.path.join(self._get_library_path(), 'EMS_conversion',
                                 'default_setting.json')
        config = {'Main': self._get_main_parameters(),
                  'Filter': self.filter_widget.get_parameters()}
        with open(fname, 'w') as outfile:
            json.dump(config, outfile)

    def _set_main_parameters(self, directory=None, subdirectory=None):
        if directory is None:
            directory = os.getcwd()
        self.dname = directory
        if subdirectory is not None:
            self.set_subdirectory(subdirectory)

    def _get_main_parameters(self):
        self.main_parameters = {'directory': self.dname,
                                'subdirectory': self.get_subdirectory()}
        return self.main_parameters

    def _update_subdirectory(self):
        self.set_subdirectory(self.SubdirectoryCheckBox.isChecked())
        self.refresh_table()

    def _on_valided_current_folder(self):
        dname = self.current_folderLineEdit.text()
        if os.path.exists(dname):
            self.filter_widget.dname = self.current_folderLineEdit.text()
            self.refresh_table()
        else:
            QtWidgets.QMessageBox.about(self, "Wrong path", "Path doesn't exist.")

    def get_files_lists(self):
        self.filter_widget.update_files_lists()
        self.files_to_use_list, self.files_to_ignore_list = self.filter_widget.get_files_lists()
        return self.files_to_use_list, self.files_to_ignore_list

    def set_subdirectory(self, value):
        self.main_parameters['subdirectory'] = value
        self.SubdirectoryCheckBox.setChecked(value)

    def get_subdirectory(self):
        return self.main_parameters['subdirectory']

    def set_filter_parameters(self, **params):
        self.filter_widget.set_parameters(**params)

    @property
    def dname(self):
        return self.filter_widget.dname

    @dname.setter
    def dname(self, value):
        if value is not None:
            self.main_parameters['directory'] = os.path.expanduser(value)
            self.current_folderLineEdit.setText(value)
            self.filter_widget.dname = value

    def _load_config_dialog(self):
        dname0 = self.dname
        fname = str(QtWidgets.QFileDialog.getOpenFileName(self, directory=dname0,
                                                      filter='*.json')[0])
        if fname == '':
            return
        else:
            self.load_config(fname=fname)

    def _save_config_dialog(self):
        dname0 = self.dname
        fname = str(QtWidgets.QFileDialog.getSaveFileName(self, directory=dname0,
                                                      filter='*.json')[0])
        if fname == '':
            return
        else:
            self._save_config(fname=fname)

    def _open_directory_dialog(self):
        dname0 = self.dname
        dname = str(
            QtWidgets.QFileDialog.getExistingDirectory(
                self, directory=dname0))
        if dname == '':
            dname = dname0
        self.dname = dname
        self.refresh_table()

    def refresh_table(self):
        self.get_files_lists()
        self.fill_tables()

    def update_table_processed_file(self, file_list):
        self.fill_tables(file_list)

    def run_threaded_process(self, files_list, function):
        process_thread = ProcessThread(self, files_list, function)
        total = len(process_thread.files_list)
        if total > 0:
            progressbarWidget = ThreadedProgressBar(self, process_thread, total)
            progressbarWidget.show()
            progressbarWidget.thread.start()
        else:
            print("No file to convert.")
            QtWidgets.QMessageBox.about(
                self, "Empty file list", "The file list is empty."
                )


class ProcessThread(QtCore.QThread):

    update = QtCore.Signal()

    def __init__(self, parent, files_list, function):
        super().__init__(parent)
        self.parent = parent
        self.files_list = files_list
        self.function = function
        self.threadactive = True

    def run(self):
        file_list = self.files_list.copy()
        print(file_list)
        for i, filename in enumerate(self.files_list):
            if not self.threadactive:
                print("Processing canceled.")
                break
            print(f'Process file #{i}: {filename}')
            self.function(filename)
            file_list.remove(filename)
            self.parent.update_table_processed_file(file_list)
            self.update.emit()
        self.finished.emit()

    def stop(self):
        self.threadactive = False
        self.wait()
