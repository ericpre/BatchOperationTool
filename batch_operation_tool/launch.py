# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 21:35:45 2015

@author: eric
"""
import sys
from python_qt_binding import QtGui
#from PyQt4 import QtGui

from batch_operation_tool.batch_operation_tool_ui import get_batch_operation_widget

def main():
    app = QtGui.QApplication(sys.argv)
    
    batch_operation_widget = get_batch_operation_widget()
    batch_operation_widget.show()

    app.exec_()    

if __name__ == '__main__':
    main()
