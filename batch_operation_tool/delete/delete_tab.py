# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 16:59:12 2015

@author: eric
"""
from python_qt_binding import QtGui

from batch_operation_tool.base_tab.base_tab import BaseTab	
from batch_operation_tool.delete.filter_widget import FilterWidget
from batch_operation_tool.delete.delete import delete_files_list_function

class DeleteTab(BaseTab):
    def __init__(self, fill_tables, parent=None):
        """ Need to pass the fill_tables method from parent class"""
        super(DeleteTab, self).__init__(fill_tables=fill_tables, parent=parent)
#        self._initUI()
#        self._init_main_parameters()
#        self.fill_tables = fill_tables
        
    def _initUI(self):
        self.filter_widget = FilterWidget(parent=self)

        self.SelectFolderButton = QtGui.QPushButton('Select folder', self)
        self.SubdirectoryCheckBox = QtGui.QCheckBox('Subdirectory:', self)
        self.OperationApplyButton = QtGui.QPushButton('Delete files', self)    
        self.LoadConfigButton = QtGui.QPushButton('Load config', self)  
        self.SaveConfigButton = QtGui.QPushButton('Save config', self)  

        # layout
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.SelectFolderButton)
        hbox1.addWidget(self.SubdirectoryCheckBox)
        hbox1.addWidget(self.OperationApplyButton)
        hbox1.addWidget(self.LoadConfigButton)
        hbox1.addWidget(self.SaveConfigButton)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addWidget(self.filter_widget)
        self.setLayout(vbox)

        self._connect_ui()

    def _connect_ui(self):
        self.SelectFolderButton.clicked.connect(self._open_directory_dialog)
        self.SubdirectoryCheckBox.clicked.connect(self._update_subdirectory)                     
        self.OperationApplyButton.clicked.connect(self._delete_files)
        self.LoadConfigButton.clicked.connect(self._load_config_dialog)
        self.SaveConfigButton.clicked.connect(self._save_config_dialog)
        
    def _delete_files(self):
        # Add dialog box to confirm?
#        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
#        buttonBox.show()
        files_list = self.get_files_lists()[0]      
        delete_files_list_function(files_list)