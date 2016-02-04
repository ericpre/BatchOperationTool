# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 21:35:45 2015

@author: eric
"""
import sys
from python_qt_binding import QtGui

from batch_operation_tool.batch_operation_tool_ui import BatchOperationToolUI

def main():
    app = QtGui.QApplication(sys.argv)
    batch_operation_widget = BatchOperationToolUI()
    batch_operation_widget.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
#    sys.path.append(os.path.dirname(__file__))
    main()