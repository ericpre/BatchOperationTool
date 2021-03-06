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

import sys
import os
from qtpy import QtWidgets


class BatchOperationToolUI(QtWidgets.QWidget):

    def __init__(self, window_title='Batch Operation Tool',
                 load_settings='default', parent=None):
        super(BatchOperationToolUI, self).__init__(parent=parent)

        self._initUI(window_title=window_title, load_settings=load_settings)

    def _initUI(self, window_title, load_settings='default'):
        # window
        self.setGeometry(300, 300, 800, 1000)
        self.setWindowTitle(window_title)

        self._create_tables_widget()
        self._create_header_tabs()

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.headers_tab)
        vbox.addWidget(self.tables_widget)
        self.setLayout(vbox)

        self._connect_ui()

    def add_tab(self, widget, load_settings='default', **kwargs):
        # Create the widget instance
        tab_widget = widget(fill_tables=self.fill_tables,
                            parent=self, **kwargs)
        # Create the widget instance to the QTabWidget
        self.tab[tab_widget.name] = tab_widget
        self.headers_tab.addTab(tab_widget, tab_widget.name)
        if load_settings == 'default':
            tab_widget.load_config()
        elif load_settings == None:
            pass
        else:
            raise ValueError(
                "Load settings argument incorrect, should be None or 'default'")

    def _connect_ui(self):
        self.headers_tab.currentChanged.connect(self.fill_tables)
#        self.keyPressEvent = self._delete_active_raw_on_event

    def _create_header_tabs(self):
        self.headers_tab = QtWidgets.QTabWidget()
        self.tab = {}

    def _create_tables_widget(self):
        self._setup_tables()
        self.tables_widget = QtWidgets.QTabWidget()     # add tab
        self.tables_widget.addTab(self.files_table, "Files")
        self.tables_widget.addTab(self.ignore_table, "Ignored files")

    def _setup_tables(self):
        self.files_table = QtWidgets.QTableWidget()
        self._setup_table(self.files_table)
        self.ignore_table = QtWidgets.QTableWidget()
        self._setup_table(self.ignore_table)

    def _setup_table(self, table):
        table.setColumnCount(3)
        table.horizontalHeader().setStretchLastSection(True)
        table.setHorizontalHeaderLabels(['Path', 'Directory', 'File'])

    def fill_tables(self, file_list=None):
        if file_list is not None and type(file_list) is list:
            self._fill_table(self.files_table, file_list)
            return
        current_tab_widget = self._get_current_tab_widget()
        (file_to_use_list, files_to_ignore_list) = current_tab_widget.get_files_lists()
        self._fill_table(self.files_table, file_to_use_list)
        self._fill_table(self.ignore_table, files_to_ignore_list)

    def _fill_table(self, table, files_list):
        table.setRowCount(len(files_list))
        for i, fullfilename in enumerate(files_list):
            fulldirname, filename = os.path.split(fullfilename)
            path, dirname = os.path.split(fulldirname)
            table.setItem(i, 0, QtWidgets.QTableWidgetItem(path))
            table.setItem(i, 1, QtWidgets.QTableWidgetItem(dirname))
            table.setItem(i, 2, QtWidgets.QTableWidgetItem(filename))

    def get_tab_with_name(self, name):
        return self.tab[name]

    def _get_current_tab_widget(self):
        return self.headers_tab.currentWidget()


def get_batch_operation_widget():
    batch_operation_widget = BatchOperationToolUI()

    # Add delete tab
    from batch_operation_tool.delete.delete_tab import DeleteTab
    batch_operation_widget.add_tab(DeleteTab)

    # Add EMS conversion tab
    from batch_operation_tool.EMS_conversion.EMS_conversion_tab import EMSConversionTab
    batch_operation_widget.add_tab(EMSConversionTab)

    # Add TIA conversion tab
    from batch_operation_tool.TIA_file_conversion.TIA_conversion_tab import TIAConversionTab
    batch_operation_widget.add_tab(TIAConversionTab)

    # Add bin conversion tab
    from batch_operation_tool.uSTEM_conversion.uSTEM_conversion_tab import uSTEMConversionTab
    batch_operation_widget.add_tab(uSTEMConversionTab)

    # Add copy tab
    from batch_operation_tool.copy.copy_tab import CopyTab
    batch_operation_widget.add_tab(CopyTab)

    return batch_operation_widget

if __name__ == '__main__':
    sys.path.append(os.path.dirname(__file__))
    app = QtWidgets.QApplication(sys.argv)

    batch_operation_widget = get_batch_operation_widget()
    batch_operation_widget.show()

    sys.exit(app.exec_())
