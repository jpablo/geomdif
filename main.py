#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
import imp
import sys

#PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
#path = os.path.join(PROJECT_PATH, '..')
#os.environ['PYTHONPATH'] += path + ";"

#from pivy.gui.soqt import SoQt,  SoQtViewer
#from superficie.util import connect
Quarter = True


from PyQt4 import QtCore, QtGui, uic
import orden
import superficie
from superficie.util import conecta

#SoInput.addDirectoryFirst("modulos")

def __import__(moduleName):
    """imports a module programatically"""
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
    """The main window of the program"""
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
        ## El programa solo tiene dos "módulos":
        ## la presentación y el visor.
        ## Todos los capítulos se agregan y son manejados por
        ## el módulo "Viewer". Solamente se agrega una entrada a la lista de módulos
        ## por cada capítulo, y se selecciona el capítulo adecuado cuando se hace
        ## click en la linea correspondiente.
        ## Esto es para evitar tener decenas de visores de OpenInventor
        ## ============================
        self.creaModulo("Presentacion", True)

        self.viewer = self.creaModulo("superficie.viewer.Viewer")
        #self.viewer = self.creaModulo("superficie.viewer")
        self.viewer.setColorLightOn(False)
        self.viewer.setWhiteLightOn(False)
#        self.viewer.trackCameraPosition(True)
        ## ============================

        #from superficie import book
        from superficie.book import Book
        for chapterName in orden.orden:
            module = __import__(chapterName)
            Chapter = getattr(module, chapterName)
            ## nos aseguramos que Chapter implemente la interfaz mínima
            #if not issubclass(Chapter, superficie.book.chapter.Chapter):
            if not issubclass(Chapter, superficie.book.Chapter):
                continue
            chapter = Chapter()
            self.viewer.addChapter(chapter)
            self.viewer.whichPage = 0

#            chapter.pageChanged.connect(self.viewer.viewAll)
            self.contenidosList.addItem(chapter.name)
            self.viewer.whichChapter = 0


    def creaModulo(self, path, addList = False):
        ## Exáctamente qué es un módulo?
        ## Es un modulo de python con una clase derivada de QtGui.QWidget que se llama
        ## igual que el módulo. Esta clase tiene el constructor:
        ##  def __init__(self,parent=None,uiLayout=None, ...)
        ## y un atributo "name"
        ## ==================================
        module = __import__(path)
        ## ==================================
        uiLayout  =  QtGui.QVBoxLayout()
        notasLayout  =  QtGui.QVBoxLayout()
        ## ==================================
        ## se usa la convención de que la clase se llama igual que el módulo
        ## p.ej. si path == "superficie.Viewer", se asume que dentro de Viewer existe
        ## una clase "Viewer"
        name = path.split(".")[-1]
        moduloW = getattr(module,name)(self.modulosStack,uiLayout,notasLayout)
        self.modulosStack.addWidget(moduloW)
        if addList:
            self.contenidosList.addItem(moduloW.name)
        ## ==================================
        controles = QtGui.QWidget()
        controles.setLayout(uiLayout)
        notas = QtGui.QWidget()
        notas.setLayout(notasLayout)
        ## ==================================
        self.controlesStack.addWidget(controles)
        self.notasStack.addWidget(notas)
        return moduloW

    @QtCore.pyqtSignature("int")
    def on_contenidosList_currentRowChanged(self,i):
        if not i:
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

#    @QtCore.pyqtSignature("")
#    def on_actionTalCual_triggered(self):
#        w = self.modulosStack.currentWidget()
#        if hasattr(w, "setDrawStyle"):
#            w.setDrawStyle(SoQtViewer.VIEW_AS_IS)
#
#    @QtCore.pyqtSignature("")
#    def on_actionLineas_triggered(self):
#        w = self.modulosStack.currentWidget()
#        if hasattr(w, "setDrawStyle"):
#            w.setDrawStyle(SoQtViewer.VIEW_LINE)
#
#    @QtCore.pyqtSignature("")
#    def on_actionMallaSobrepuesta_triggered(self):
#        w = self.modulosStack.currentWidget()
#        if hasattr(w, "setDrawStyle"):
#            w.setDrawStyle(SoQtViewer.VIEW_WIREFRAME_OVERLAY)
#
#    @QtCore.pyqtSignature("")
#    def on_actionLineasOcultas_triggered(self):
#        w = self.modulosStack.currentWidget()
#        if hasattr(w, "setDrawStyle"):
#            w.setDrawStyle(SoQtViewer.VIEW_HIDDEN_LINE)

    def on_actionAntialiasing_toggled(self, b):
        for w in self.getModulosW():
            if hasattr(w, "viewer"):
                w.viewer.setAntialiasing(b, 1)

    @QtCore.pyqtSignature("")
    def on_actionAjusteEstereo_triggered(self):
        ## esto no funciona!!!
        if self.estereo is None:
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

#    def on_actionEstereo_toggled(self, b):
#        for w in self.getModulosW():
#            if hasattr(w, "viewer"):
#                if b:
#                    w.viewer.setStereoType(SoQtViewer.STEREO_QUADBUFFER)
#                    ## en el resto del mundo
##                    w.viewer.setStereoType(SoQtViewer.STEREO_ANAGLYPH)
#                else:
#                    w.viewer.setStereoType(SoQtViewer.STEREO_NONE)

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
    exec texto
    exec("setattr(MainWindow, 'on_action%s_triggered', on_action%s_triggered)" % (t, t))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow(None)
    viewer = window.modulosStack.widget(1)
    window.show()
    sys.exit(app.exec_())
