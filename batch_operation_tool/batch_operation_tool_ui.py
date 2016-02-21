# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 17:59:54 2015

@author: eric

TODO:
    - display the file path
    - a few TODO in the code
    - When a file is deleted, add it to the ignore list
    - Add checkBox to unselect files
    - Add progress bar
"""

import sys, os
from python_qt_binding import QtGui  # new imports
# http://cyrille.rossant.net/making-pyqt4-pyside-and-ipython-work-together/
from batch_operation_tool.EMS_file_conversion.EMS_conversion_tab import EMSConversionTab
from batch_operation_tool.delete.delete_tab import DeleteTab
from batch_operation_tool.TIA_file_conversion.TIA_conversion_tab import TIAConversionTab

class BatchOperationToolUI(QtGui.QWidget):    
    def __init__(self, window_title='Batch Operation Tool',
                 load_settings='default', parent=None):
        super(BatchOperationToolUI, self).__init__(parent=parent)

        self._initUI(window_title=window_title, load_settings=load_settings)
        
    def _initUI(self, window_title, load_settings='default'):
        # window
        self.setGeometry(300, 300, 800, 1000)
        self.setWindowTitle(window_title)

        self._create_tables_widget()
        self._create_header_tabs(load_settings=load_settings)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.headers_tab)
        vbox.addWidget(self.tables_widget)
        self.setLayout(vbox)
        
        self._connect_ui()

    def _connect_ui(self):
        self.headers_tab.currentChanged.connect(self.fill_tables)
#        self.keyPressEvent = self._delete_active_raw_on_event

    def _create_header_tabs(self, load_settings='default'):
        self.headers_tab = QtGui.QTabWidget()
        self.ems_conversion_tab = EMSConversionTab(fill_tables=self.fill_tables,
                                                   parent=self)
        self.delete_tab = DeleteTab(fill_tables=self.fill_tables, parent=self)
        self.tia_conversion_tab = TIAConversionTab(fill_tables=self.fill_tables, parent=self)

        self.headers_tab.addTab(self.tia_conversion_tab, "TIA file conversion") 
        self.headers_tab.addTab(self.delete_tab, "Delete files") 
        self.headers_tab.addTab(self.ems_conversion_tab, "EMS file conversion")   
        if load_settings == 'default':
            self.tia_conversion_tab.load_config()
            self.delete_tab.load_config()
            self.ems_conversion_tab.load_config()
        elif load_settings == None:
            pass
        else:
            raise ValueError("Load settings argument incorrect, should be None or 'default'") 

    def _create_tables_widget(self):
        self._setup_tables()
        self.tables_widget = QtGui.QTabWidget()     # add tab
        self.tables_widget.addTab(self.files_table, "Files")   
        self.tables_widget.addTab(self.ignore_table, "Ignored files")

    def _setup_tables(self):
        self.files_table = QtGui.QTableWidget()
        self._setup_table(self.files_table)
        self.ignore_table = QtGui.QTableWidget()
        self._setup_table(self.ignore_table)
        
    def _setup_table(self, table):
        table.setColumnCount(3)
        table.horizontalHeader().setStretchLastSection(True)
        table.setHorizontalHeaderLabels(['Path', 'Directory', 'File'])  

    def fill_tables(self):
        current_tab_widget = self._get_current_tab_widget()
        (file_to_use_list, files_to_ignore_list) = current_tab_widget.get_files_lists()
        self._fill_table(self.files_table, file_to_use_list)
        self._fill_table(self.ignore_table, files_to_ignore_list)
        
    def _fill_table(self, table, files_list):
        table.setRowCount(len(files_list))
        for i, fullfilename in enumerate(files_list):
            fulldirname, filename = os.path.split(fullfilename)
            path, dirname = os.path.split(fulldirname)
            table.setItem(i, 0, QtGui.QTableWidgetItem(path))
            table.setItem(i, 1, QtGui.QTableWidgetItem(dirname))
            table.setItem(i, 2, QtGui.QTableWidgetItem(filename))

    def _get_current_tab_widget(self):
        return self.headers_tab.currentWidget()        

if __name__ == '__main__':
    sys.path.append(os.path.dirname(__file__))
    app = QtGui.QApplication(sys.argv)
    batch_operation_widget = BatchOperationToolUI()
    batch_operation_widget.show()

    sys.exit(app.exec_())
