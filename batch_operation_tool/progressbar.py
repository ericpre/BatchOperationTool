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
        self.threadactive = True
        self.n = n

    def run(self):
        i = 0
        while (i<self.n):
            if not self.threadactive:
                break
            time.sleep(0.01)
            i+=1
            self.update.emit()
            print(i)

    def stop(self):
        self.threadactive = False
        self.wait()


class ThreadedProgressBar(QtWidgets.QProgressDialog):

    def __init__(self, parent, thread, total):
        super().__init__(parent)
        self.setValue(0)

        self.thread = thread
        self.total = total
        self.factor = 100 / self.total

        self.thread.update.connect(self.update)
        self.thread.finished.connect(self.close)
        self.canceled.connect(self.thread.stop)

        self.n = 0
        self.n_percent = 0

    def update(self):
        self.n += 1
        self.n_percent = self.n * self.factor
        self.setValue(self.n_percent)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    thread = Thread(parent=None, n=500)
    progressWidget = ThreadedProgressBar(None, thread, total=thread.n)
    progressWidget.move(300, 300)
    progressWidget.show()
    progressWidget.thread.start()
    app.exec_()
    # sys.exit(app.exec_())