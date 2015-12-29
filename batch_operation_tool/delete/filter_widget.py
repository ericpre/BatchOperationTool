# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 17:16:09 2015

@author: eric
"""
from python_qt_binding import QtGui

from batch_operation_tool.base_tab.filter_widget_base import FilterWidgetBase

class FilterWidget(FilterWidgetBase):
    """ Handle filters header """
    def __init__(self, parent=None):
        super(FilterWidget, self).__init__(parent=parent)

    def _init_parameters(self):
        self.parameters = {'string_list':[''],
                           'extension_list':[''],
                           'ignore_string_bool':False,
                           'ignore_string_list':[''],
                           'ignore_string_path_bool':False,
                           'ignore_string_path_list':[''],
                           'ignore_filename_extension_bool':False,
                           'ignore_filename_extension_list':['']}

    def _create_filter_groupBox(self):
        groupBox = QtGui.QGroupBox("Filter")

        label1 = QtGui.QLabel('Files containing the following string(s):', self)
        label2 = QtGui.QLabel('With the extension(s):', self)
        self.ignoreStringCheckBox = QtGui.QCheckBox('Ignore files containing string(s):', self)
        self.ignoreStringPathCheckBox = QtGui.QCheckBox('Ignore files with string(s) in path:', self)

        self.stringLineEdit = QtGui.QLineEdit(self)
        self.extentionLineEdit = QtGui.QLineEdit(self)
        self.ignoreStringLineEdit = QtGui.QLineEdit(self)
        self.ignoreStringPathLineEdit = QtGui.QLineEdit(self)

        self.ignorefilenameextensionCheckBox = QtGui.QCheckBox("Ignore if same filename doesn't exist with following extension:", self)
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
        # Connect LineEdit
        self.stringLineEdit.textChanged.connect(self.update_tables)
        self.extentionLineEdit.textChanged.connect(self.update_tables)
        self.ignoreStringLineEdit.textChanged.connect(self.update_tables)
        self.ignoreStringPathLineEdit.textChanged.connect(self.update_tables)        
        self.ignorefilenameextensionLineEdit.textChanged.connect(self.update_tables)        
        # Connect CheckBox
        self.ignoreStringCheckBox.clicked.connect(self.update_tables)
        self.ignoreStringPathCheckBox.clicked.connect(self.update_tables)
        self.ignorefilenameextensionCheckBox.clicked.connect(self.update_tables)
        
    def set_parameters(self, string_list=None, extension_list=None,
                       ignore_string_bool=None, ignore_string_list=None,
                       ignore_string_path_bool=None, ignore_string_path_list=None,
                       ignore_filename_extension_bool=None,
                       ignore_filename_extension_list=None):
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
            self.ignoreStringPathLineEdit.setText(', '.join(ignore_string_path_list))
        if ignore_filename_extension_bool is not None:
            self.ignorefilenameextensionCheckBox.setChecked(ignore_filename_extension_bool)
        if ignore_filename_extension_list is not None:
            self.ignorefilenameextensionLineEdit.setText(', '.join(ignore_filename_extension_list))

    def get_parameters(self):
        self.parameters['string_list'] = self.stringLineEdit.text().split(', ')
        self.parameters['extension_list'] = self.extentionLineEdit.text().split(', ')
        self.parameters['ignore_string_bool'] = self.ignoreStringCheckBox.isChecked()
        self.parameters['ignore_string_list'] = self.ignoreStringLineEdit.text().split(', ')
        self.parameters['ignore_string_path_bool'] = self.ignoreStringPathCheckBox.isChecked()
        self.parameters['ignore_string_path_list'] = self.ignoreStringPathLineEdit.text().split(', ')
        self.parameters['ignore_filename_extension_bool'] = self.ignorefilenameextensionCheckBox.isChecked()
        self.parameters['ignore_filename_extension_list'] = self.ignorefilenameextensionLineEdit.text().split(', ')
        return self.parameters