import Test
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
#from pivy.gui.soqt import *
from pivy.coin import *
from superficie.util import main

class Cubo(object):
    def __init__(self):
        self.root = SoCube()
        self.name = "Cubo"
        self.text = "Un cubo"


class Test(object):
    name = u"Test"
    def __init__(self,parent=None,uilayout=None):
        self.parent = parent
        self.viewAlloriginal = self.parent.viewer.viewAll
        self.objetos = []
        self.setupGui()
        self.setupPages()

    def getPages(self):
        return self.objetos
    
    def chapterSpecific(self):
        self.parent.lucesColor.whichChild = SO_SWITCH_NONE
        self.parent.lucesBlanca.on = True
        self.parent.viewer.setTransparencyType(SoGLRenderAction.SORTED_LAYERS_BLEND)
        self.parent.setDrawStyle(SoQtViewer.VIEW_AS_IS)

    def getGui(self):
        return self.gui

    def setupGui(self):
        pass

    def setupPages(self):
        ## ==============
        ## Una clase de python
        ## con un atributo root de openinventor
        cubo = Cubo()
        self.objetos.append(cubo)
        ## ==================
        ## un objeto de openinventor directamente
        esfera = SoSphere()
        self.objetos.append(esfera)



if __name__ == "__main__":
    app = main(sys.argv)

    window = Simetrias3D()
    window.resize(700,700)
    window.rotor.on = False
    window.show()
    window.ui.show()
    SoQt.mainLoop()
