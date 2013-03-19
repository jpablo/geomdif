# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore, uic
from superficie.book import Chapter, Page


class Presentacion(QtGui.QWidget):
    u"""
    <p>
    Primero mostramos curvas parametrizadas para ilustrar los conceptos de vector
    tangente, curvatura y torsión.
    <p>
    Luego vemos curvas en superficies para llegar al concepto de plano tangente en
    un punto, parametrizamos varias superficies y mostramos la relación entre el
    plano tangente y la superficie en puntos de los diversos tipos.
    <p>
    Después ilustramos el concepto de sección normal para motivar el de curvatura
    de una superficie en un punto.
    <p>
    Mostramos superficies distintas con la misma curvatura gaussiana (isométricas)
    y la no orientabilidad de la banda de Möbius.
    <p>
    Finalizamos con ejemplos de campos vectoriales tangentes en distintas
    superficies que permiten llegar al concepto de índice de un campo en una
    singularidad del campo.
    """
    name = u"Presentación"

    def __init__(self, parent=None, uilayout=None, noteslayout=None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("ui/presentacion.ui", self)

        notes = QtGui.QLabel(self.__doc__)
        notes.setWordWrap(True)
        notes.setTextFormat(QtCore.Qt.RichText)
        sa = QtGui.QScrollArea()
        sa.setWidget(notes)
        sa.setWidgetResizable(True)
        sa.setFrameStyle(QtGui.QFrame.Plain)
        noteslayout.addWidget(sa)



