from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem
from PyQt5 import uic
import sys
import paramiko
class view(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("View cache\View.ui",self)

        horHeaders = ["URL", "IP Address"]
        self.cache.setColumnCount(2)
        self.cache.setHorizontalHeaderLabels(horHeaders)

        self.columnview.setRowCount(len(cache))
        count = 0

        for i in b:
            c = i.split(",")
            item0 = QTableWidgetItem(str(c[0]))
            item1 = QTableWidgetItem(str(c[1]))
            self.columnview.setItem(count,0,item0)
            self.columnview.setItem(count,0,item1)
            count += 1

def launch(cache):
    app = QApplication(sys.argv)
    View= view()
    View.show()
    app.exec_()
