import sys, re, os
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem, QFileDialog
from PyQt5 import uic


class language(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("Main Window\Main.ui",self) #cargando archivo.ui

    def spanish(self):
        self.Maintab.setTabText(0,"Inicio")
        self.Maintab.setTabText(1,"Ethernet y routing")
        self.Maintab.setTabText(4,"Sis. Admin.")
        self.Maintab.setTabText(5,"Acerca de..")
        print("hola")

    def english(self):
        self.Maintab.setTabText(0,"Home")
        self.Maintab.setTabText(1,"Ethernet and routing")
        self.Maintab.setTabText(4,"Sys. Admin.")
        self.Maintab.setTabText(5,"About")

#app = QApplication(sys.argv)
#dialogo.hide()
#app.exec_()
