#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 20:32:45 2018

@author: eric
"""

from qtpy import QtCore, QtWidgets
import time
 
class Thread(QtCore.QThread):

    update = QtCore.Signal()

    def __init__(self, parent, n):
        super().__init__(parent)
        self.n = n

    def run(self):
        i = 0
        while (i<self.n):
            time.sleep(0.01)
            i+=1
            self.update.emit()


class ThreadedProgressBar(QtWidgets.QProgressDialog):

    def __init__(self, parent, thread): 
        super().__init__(parent)
        # Set up the user interface from Designer. 
        self.setValue(0)

        self.thread = thread

        self.thread.update.connect(self.update)
        self.thread.finished.connect(self.close)

        self.n = 0

    def update(self):
        self.n += 1
        self.setValue(self.n)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    thread = Thread(parent=None, n=100)
    progressWidget = ThreadedProgressBar(None, thread)
    progressWidget.move(300, 300)
    progressWidget.show()
    progressWidget.thread.start()
    app.exec_()
    # sys.exit(app.exec_())