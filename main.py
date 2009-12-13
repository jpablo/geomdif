#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

from superficie.util import connect
import imp
import sys
#from pivy.gui.soqt import SoQt,  SoQtViewer

try:
    from pivy.quarter import QuarterWidget
    Quarter = True
except ImportError:
    from pivy.gui.soqt import *
    Quarter = False


from PyQt4 import QtCore, QtGui, uic
import orden
import superficie.base
from superficie.util import main,  conecta

#SoInput.addDirectoryFirst("modulos")

def __import__(moduleName):
    "importa un módulo de forma programática"
    pathList = moduleName.split(".")
    path = None
    module = None
    for name in pathList:
        fp, pathname, description = imp.find_module(name,path)
        try:
            module =  imp.load_module(name, fp, pathname, description)
            path = getattr(module,"__path__",None)
        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()
    return module


class MainWindow(QtGui.QMainWindow):
    "Implementacion de la ventana principal"
    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        uic.loadUi("ui/mainwindow2.ui", self)
        ## por alguna razon no toma en cuenta
        ## las opciones del designer, así que hay que
        ## hacerlo a mano
#        self.actionRotar.setCheckable(True)
#        self.actionRotar.setChecked(True)
        self.parent = None
        ## ============================
        self.npasses = 0
        self.aasmothing = True
        self.estereo = None
        ## ============================
        self.initModules()
        self.setWindowTitle(u"Geometría Diferencial")
        self.setWindowIcon(QtGui.QIcon(":/iconos/icono1.jpg"))

    def initModules(self):
        ## self.contenidosList
        ## self.controlesStack
        ## self.modulosStack
        ## self.notasStack
        ## ============================
        ## designer le pone una página a los stacks
        for name in ["notas", "controles","modulos"]:
            stack = getattr(self,name+"Stack")
            stack.removeWidget(stack.widget(0))
        ## ============================
        ## El programa solo tiene dos "módulos":
        ## la presentación y el visor.
        ## Todos los capítulos se agregan y son manejados por
        ## el módulo "Viewer". Solamente se agrega una entrada a la lista de módulos
        ## por cada capítulo, y se selecciona el capítulo adecuado cuando se hace
        ## click en la linea correspondiente.
        ## Esto es para evitar tener decenas de visores de OpenInventor
        ## ============================
        self.creaModulo("Presentacion", True)
        self.viewer = self.creaModulo("superficie.Viewer")
        self.viewer.setColorLightOn(False)
        self.viewer.setWhiteLightOn(False)
        self.viewer.trackCameraPosition(True)
        def func(i):
            print "func:", i

        ## Esto marca un error
#        self.viewer.chapterChanged.connect(func)
        ## ============================
        for chapterName in orden.orden:
            print "chapterName:", chapterName
            module = __import__(chapterName)
            Chapter = getattr(module, chapterName)
            ## nos aseguramos que Chapter implemente la interfaz mínima
            if not issubclass(Chapter, superficie.base.Chapter):
                continue
            chapter = Chapter()
            self.viewer.addChapter(chapter)
#            chapter.pageChanged.connect(self.viewer.viewAll)
            self.contenidosList.addItem(chapter.name)
            self.viewer.whichPage = 0

    def creaModulo(self, path, addList = False):
        ## Exáctamente qué es un módulo?
        ## Es un modulo de python con una clase derivada de QtGui.QWidget que se llama
        ## igual que el módulo. Esta clase tiene el constructor:
        ##  def __init__(self,parent=None,uiLayout=None, ...)
        ## y un atributo "name"
        ## ==================================
        module = __import__(path)
        ## ==================================
        layout1  =  QtGui.QVBoxLayout()
        layout2  =  QtGui.QVBoxLayout()
        ## ==================================
        ## se usa la convención de que la clase se llama igual que el módulo
        ## p.ej. si path == "superficie.Viewer", se asume que dentro de Viewer existe
        ## una clase "Viewer"
        name = path.split(".")[-1]
        moduloW = getattr(module,name)(self.modulosStack,layout1)
        self.modulosStack.addWidget(moduloW)
        if addList:
            self.contenidosList.addItem(moduloW.name)
        ## ==================================
        controles = QtGui.QWidget()
        controles.setLayout(layout1)
        notas = QtGui.QWidget()
        notas.setLayout(layout2)
        ## ==================================
        self.controlesStack.addWidget(controles)
        self.notasStack.addWidget(notas)
        return moduloW

    @QtCore.pyqtSignature("int")
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
            viewer.whichChapter = i-1

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
    app = QtGui.QApplication(sys.argv)
    window = MainWindow(None)
    viewer = window.modulosStack.widget(1)
    window.show()
    if Quarter:
        sys.exit(app.exec_())
    else:
        SoQt.mainLoop()
