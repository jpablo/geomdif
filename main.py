#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys
from pivy.gui.soqt import SoQt,  SoQtViewer
from PyQt4 import QtCore, QtGui, uic
import orden
from superficie.util import main,  conecta

def mezcla(ob, window, *attrs):
    "copia los atributos especificados: window ==> ob"
    for at in attrs:
        setattr(ob, at, window.child(at))

#SoInput.addDirectoryFirst("modulos")

class MainWindow(QtGui.QMainWindow):
    "Implementacion de la ventana principal"
    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        uic.loadUi("ui/mainwindow.ui", self)
        ## por alguna razon no toma en cuenta
        ## las opciones del designer, así que hay que
        ## hacerl a mano
        self.actionRotar.setCheckable(True)
        self.actionRotar.setChecked(True)
        self.parent = None
        ## ============================
        self.npasses = 0
        self.aasmothing = True
        self.estereo = None
        ## ============================
        self.controles = []
        self.initModules()

        self.setWindowTitle(u"Geometría Diferencial")
#        self.showMaximized()
        self.setWindowIcon(QtGui.QIcon(":/iconos/icono1.jpg"))

    def initModules(self):
        ## here are defined:
        ## 
        ## self.contenidosList
        ## self.controlesStack
        ## self.notasStack
        ## 
        dock = QtGui.QDockWidget("Contenidos", self)
        self.contenidosList = QtGui.QListWidget(dock)
        dock.setWidget(self.contenidosList)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        conecta(self.contenidosList, QtCore.SIGNAL("currentRowChanged(int)"),
            self.on_contenidosList_currentRowChanged)
        ## ============================
        dock = QtGui.QDockWidget("", self)
        self.controlesStack = QtGui.QStackedWidget(dock)
        dock.setWidget(self.controlesStack)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        ## ============================
        dock = QtGui.QDockWidget("Notas", self)
        self.notasStack = QtGui.QStackedWidget(dock)
        dock.setWidget(self.notasStack)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        ## ============================
        self.creaModulo("Presentacion", True)
        ## ============================
        viewer = self.viewer = self.creaModulo("Viewer", dir="superficie")
        self.importaModulos()
        for i,modulo in enumerate(orden.orden):
            exec("import " + modulo)
            moduloOb = eval( "%s.%s(viewer)" % (modulo,modulo) )
            viewer.addChapter(moduloOb)
            if hasattr(moduloOb, "getProlog"):
                viewer.addChapterProlog(moduloOb.getProlog())
            viewer.addPageChild(moduloOb.getPages())
            viewer.whichPage = 0
            self.contenidosList.addItem(moduloOb.name)
            ## ============================
            ## creo que no se necesita
            sw = QtGui.QStackedWidget(self)
            self.notasStack.addWidget(sw)

    def importaModulos(self):
        for i,modulo in enumerate(orden.orden):
            exec("import " + modulo)

    def creaModulo(self, modulo, addList = False, dir = ""):
        controles = QtGui.QWidget()
        layout1  =  QtGui.QVBoxLayout()
        controles.setLayout(layout1)
        ## ============================
        notas = QtGui.QWidget()
        layout2  =  QtGui.QVBoxLayout()
        notas.setLayout(layout2)
        ## ==================================
        modFile = modulo if dir == "" else dir + "." + modulo
        ## ==================================
        exec("import " + modFile)
        moduloW = eval( "%s.%s(self.modulosStack,layout1,layout2)" % (modFile,modulo) )
        self.modulosStack.addWidget(moduloW)
        if addList:
            self.contenidosList.addItem(moduloW.name)
        ## ==================================
        ## just an empty widget
        self.controlesStack.addWidget(controles)
        self.notasStack.addWidget(notas)
        return moduloW

    def on_contenidosList_currentRowChanged(self,i):
        if i == 0:
            self.modulosStack.setCurrentIndex(0)
            self.controlesStack.setCurrentIndex(0)
            self.notasStack.setCurrentIndex(0)
        else:
            self.modulosStack.setCurrentIndex(1)
            self.controlesStack.setCurrentIndex(1)
            self.notasStack.setCurrentIndex(1)
            viewer = self.modulosStack.widget(1)
            viewer.setWhichChapter(i-1)

    def getModulosW(self):
        return [self.modulosStack.widget(i) for i in range(self.modulosStack.count())]

    def on_actionRotar_toggled(self, b):
        for w in self.getModulosW():
            if hasattr(w, "rotor"):
                w.rotor.on = b

    @QtCore.pyqtSignature("")
    def on_actionTalCual_triggered(self):
        w = self.modulosStack.currentWidget()
        if hasattr(w, "setDrawStyle"):
            w.setDrawStyle(SoQtViewer.VIEW_AS_IS)

    @QtCore.pyqtSignature("")
    def on_actionLineas_triggered(self):
        w = self.modulosStack.currentWidget()
        if hasattr(w, "setDrawStyle"):
            w.setDrawStyle(SoQtViewer.VIEW_LINE)

    @QtCore.pyqtSignature("")
    def on_actionMallaSobrepuesta_triggered(self):
        w = self.modulosStack.currentWidget()
        if hasattr(w, "setDrawStyle"):
            w.setDrawStyle(SoQtViewer.VIEW_WIREFRAME_OVERLAY)

    @QtCore.pyqtSignature("")
    def on_actionLineasOcultas_triggered(self):
        w = self.modulosStack.currentWidget()
        if hasattr(w, "setDrawStyle"):
            w.setDrawStyle(SoQtViewer.VIEW_HIDDEN_LINE)

    def on_actionAntialiasing_toggled(self, b):
        for w in self.getModulosW():
            if hasattr(w, "viewer"):
                w.viewer.setAntialiasing(b, 1)

    @QtCore.pyqtSignature("")
    def on_actionAjusteEstereo_triggered(self):
        ## esto no funciona!!!
        if self.estereo == None:
            self.estereo = uic.loadUi("estereo.ui")
#            self.estereo.ajusteEstereo.setMaximum(50)
#            self.estereo.ajusteEstereo.setValue(50 * .075)
#            conecta(self.estereo.ajusteEstereo, QtCore.SIGNAL("valueChanged(int)"), self.setStereoAdjustment)
            ## ============================
            self.estereo.ajusteEstereo.setMinimum(20)
            self.estereo.ajusteEstereo.setMaximum(50)
            self.estereo.ajusteEstereo.setValue(30)
            conecta(self.estereo.ajusteEstereo, QtCore.SIGNAL("valueChanged(int)"), self.setPlanoOffset)
            ## ============================
        self.estereo.show()

    def setStereoAdjustment(self, n):
        for w in self.getModulosW():
            if hasattr(w, "viewer"):
                w.setStereoAdjustment(n/float(25))

    def setPlanoOffset(self, n):
        w = self.modulosStack.currentWidget()
        if hasattr(w, "setPlanoOffset"):
            w.setPlanoOffset(n/float(10))

    def on_actionEstereo_toggled(self, b):
        for w in self.getModulosW():
            if hasattr(w, "viewer"):
                if b:
                    w.viewer.setStereoType(SoQtViewer.STEREO_QUADBUFFER)
                    ## en el resto del mundo
#                    w.viewer.setStereoType(SoQtViewer.STEREO_ANAGLYPH)
                else:
                    w.viewer.setStereoType(SoQtViewer.STEREO_NONE)

    def on_actionEjes_toggled(self, b):
        for w in self.getModulosW():
            if hasattr(w, "ejes"):
                w.ejes.show(b)
    ## ============================

    def helpIndex(self):
        print "helpIndex"


tiposTransparencia = [
    "SCREEN_DOOR",
    "ADD",
    "DELAYED_ADD",
    "SORTED_OBJECT_ADD",
    "BLEND",
    "DELAYED_BLEND",
    "SORTED_OBJECT_BLEND",
    "SORTED_OBJECT_SORTED_TRIANGLE_ADD",
    "SORTED_OBJECT_SORTED_TRIANGLE_BLEND",
    "NONE",
    "SORTED_LAYERS_BLEND"
]

## creamos las funciones que manejan la
## transparencia
for t in tiposTransparencia:
    texto = """
@QtCore.pyqtSignature("")
def on_action%s_triggered(self):
    w = self.modulosStack.currentWidget()
    print "on_action%s_triggered",  w
    if hasattr(w, "viewer"):
        w.viewer.setTransparencyType(SoGLRenderAction.%s)"""% (t, t, t)
    exec(texto)
    exec("setattr(MainWindow, 'on_action%s_triggered', on_action%s_triggered)" % (t, t))


if __name__ == "__main__":
    app = main(sys.argv)
    window = MainWindow(None)
    viewer = window.modulosStack.widget(1)
#    print "on_actionNONE_triggered" in dir(window)
    window.show()
    SoQt.mainLoop()
