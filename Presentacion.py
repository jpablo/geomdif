# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore, uic



class Presentacion(QtGui.QWidget):
    name = u"Presentación"
    def __init__(self,parent=None,uilayout=None,notaslayout=None):
        QtGui.QWidget.__init__(self,parent)
        uic.loadUi("ui/presentacion.ui",self)
