# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 14:46:36 2015

@author: eric
"""
import os
from python_qt_binding import QtGui

from batch_operation_tool.file_filter import FileFilter


class FilterWidgetBase(QtGui.QWidget):
    """ Handle filters header """

    def __init__(self, parent=None):
        super(FilterWidgetBase, self).__init__(parent=parent)
        self.dname = os.getcwd()

        self.files_to_use_list = []
        self.files_to_ignore_list = []

        self._init_widget()
        self._init_parameters()

        self._connect_ui()

    def _init_widget(self):
        self.filter_groupBox = self._create_filter_groupBox()

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.filter_groupBox)
        self.setLayout(vbox)

    def _init_parameters(self):
        # To make a new plugin change here
        self.parameters = {'string_list': [''],
                           'extension_list': [''],
                           'ignore_string_bool': False,
                           'ignore_string_list': [''],
                           'ignore_string_path_bool': False,
                           'ignore_string_path_list': [''],
                           'ignore_filename_extension_bool': False,
                           'ignore_filename_extension_list': ['']}

    def _create_filter_groupBox(self):
        # To make a new plugin change here
        groupBox = QtGui.QGroupBox("Filter")

        label1 = QtGui.QLabel(
            'Files containing the following string(s):', self)
        label2 = QtGui.QLabel('With the extension(s):', self)
        self.ignoreStringCheckBox = QtGui.QCheckBox(
            'Ignore files containing string(s):', self)
        self.ignoreStringPathCheckBox = QtGui.QCheckBox(
            'Ignore files with string(s) in path:', self)

        self.stringLineEdit = QtGui.QLineEdit(self)
        self.extentionLineEdit = QtGui.QLineEdit(self)
        self.ignoreStringLineEdit = QtGui.QLineEdit(self)
        self.ignoreStringPathLineEdit = QtGui.QLineEdit(self)

        self.ignorefilenameextensionCheckBox = QtGui.QCheckBox(
            "Ignore if same filename doesn't exist with following extension:", self)
        self.ignorefilenameextensionLineEdit = QtGui.QLineEdit(self)

        # Layout
        FilterLayout = QtGui.QGridLayout()
        # 1st column
        FilterLayout.addWidget(label1, 0, 0)
        FilterLayout.addWidget(label2, 1, 0)
        FilterLayout.addWidget(self.ignoreStringCheckBox, 2, 0)
        FilterLayout.addWidget(self.ignoreStringPathCheckBox, 3, 0)
        # 2nd column
        FilterLayout.addWidget(self.stringLineEdit, 0, 1)
        FilterLayout.addWidget(self.extentionLineEdit, 1, 1)
        FilterLayout.addWidget(self.ignoreStringLineEdit, 2, 1)
        FilterLayout.addWidget(self.ignoreStringPathLineEdit, 3, 1)
        FilterLayout.addWidget(self.ignorefilenameextensionCheckBox, 4, 0)
        FilterLayout.addWidget(self.ignorefilenameextensionLineEdit, 4, 1)

        groupBox.setLayout(FilterLayout)

        return groupBox

    def _connect_ui(self):
        # To make a new plugin change here
        # Connect LineEdit
        self.stringLineEdit.textChanged.connect(self.update_tables)
        self.extentionLineEdit.textChanged.connect(self.update_tables)
        self.ignoreStringLineEdit.textChanged.connect(self.update_tables)
        self.ignoreStringPathLineEdit.textChanged.connect(self.update_tables)
        self.ignorefilenameextensionLineEdit.textChanged.connect(
            self.update_tables)
        # Connect CheckBox
        self.ignoreStringCheckBox.clicked.connect(self.update_tables)
        self.ignoreStringPathCheckBox.clicked.connect(self.update_tables)
        self.ignorefilenameextensionCheckBox.clicked.connect(
            self.update_tables)

    def set_parameters(self, string_list=None, extension_list=None,
                       ignore_string_bool=None, ignore_string_list=None,
                       ignore_string_path_bool=None, ignore_string_path_list=None,
                       ignore_filename_extension_bool=None,
                       ignore_filename_extension_list=None):
        # To make a new plugin change here
        if string_list is not None:
            self.stringLineEdit.setText(', '.join(string_list))
        if extension_list is not None:
            self.extentionLineEdit.setText(', '.join(extension_list))
        if ignore_string_bool is not None:
            self.ignoreStringCheckBox.setChecked(ignore_string_bool)
        if ignore_string_list is not None:
            self.ignoreStringLineEdit.setText(', '.join(ignore_string_list))
        if ignore_string_path_bool is not None:
            self.ignoreStringPathCheckBox.setChecked(ignore_string_path_bool)
        if ignore_string_path_list is not None:
            self.ignoreStringPathLineEdit.setText(
                ', '.join(ignore_string_path_list))
        if ignore_filename_extension_bool is not None:
            self.ignorefilenameextensionCheckBox.setChecked(
                ignore_filename_extension_bool)
        if ignore_filename_extension_list is not None:
            self.ignorefilenameextensionLineEdit.setText(
                ', '.join(ignore_filename_extension_list))

    def get_parameters(self):
        # To make a new plugin change here
        self.parameters['string_list'] = self.stringLineEdit.text().split(', ')
        self.parameters[
            'extension_list'] = self.extentionLineEdit.text().split(', ')
        self.parameters[
            'ignore_string_bool'] = self.ignoreStringCheckBox.isChecked()
        self.parameters[
            'ignore_string_list'] = self.ignoreStringLineEdit.text().split(', ')
        self.parameters[
            'ignore_string_path_bool'] = self.ignoreStringPathCheckBox.isChecked()
        self.parameters[
            'ignore_string_path_list'] = self.ignoreStringPathLineEdit.text().split(', ')
        self.parameters[
            'ignore_filename_extension_bool'] = self.ignorefilenameextensionCheckBox.isChecked()
        self.parameters[
            'ignore_filename_extension_list'] = self.ignorefilenameextensionLineEdit.text().split(', ')
        return self.parameters

    def update_files_lists(self):
        self.get_parameters()
        self.files_to_use_list = []
        self.files_to_ignore_list = []
        # Get the list of files to delete
        file_filter = FileFilter(
            self.dname, self._get_subdirectory(), **self.parameters)
        self.files_to_use_list, self.files_to_ignore_list = file_filter.get_files_lists()

    def update_tables(self):
        self.update_files_lists()
        self.parent().fill_tables()

    def get_files_lists(self):
        return self.files_to_use_list, self.files_to_ignore_list

    def _get_subdirectory(self):
        return self.parent().get_subdirectory()

    @property
    def dname(self):
        return self._dname

    @dname.setter
    def dname(self, value):
        if value is not None:
            self._dname = os.path.expanduser(value)
